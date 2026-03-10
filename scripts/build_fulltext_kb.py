"""
build_fulltext_kb.py
====================
KS TalentBridge — Full-Text Knowledge Base Builder (Layer 2)

Produces KSE_FullText_KB.jsonl — one record per unique person, containing
their complete resume text. Upload this file directly to ChatGPT for deep
narrative queries that require reading actual resume content.

Output: KSE_FullText_KB.jsonl  (TalentBridge root folder)
        KSE_FullText_KB_stats.txt (summary)
"""

import os, re, zipfile, json, sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import fitz
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False
    print("[WARN] PyMuPDF not installed — PDFs will be skipped. Run: pip install pymupdf")

# ── Config ────────────────────────────────────────────────────────────────────

_ROOT         = Path(__file__).resolve().parent.parent
RESUME_FOLDER = str(_ROOT / "data" / "source" / "Resume 08152025")
OUT_DIR       = str(_ROOT / "data" / "kb")
RESUME_EXTS   = {".docx", ".pdf", ".rtf"}
W_NS          = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# ── Text Extraction (full — no truncation) ────────────────────────────────────

def _paras_from_xml(xml_bytes):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    out = []
    for p in root.iter(f"{W_NS}p"):
        t = "".join(n.text for n in p.iter(f"{W_NS}t") if n.text).strip()
        if t:
            out.append(t)
    return out

def extract_docx(path):
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            parts = ["word/document.xml"]
            parts += sorted(n for n in names if re.match(r"word/(header|footer)\d*\.xml", n))
            parts += sorted(n for n in names if n.startswith("word/") and n.endswith(".xml")
                            and n not in parts and "theme" not in n and "settings" not in n
                            and "webSettings" not in n and "fontTable" not in n)
            paras = []
            for part in parts:
                try:
                    with z.open(part) as f:
                        paras.extend(_paras_from_xml(f.read()))
                except Exception:
                    pass
        seen, d = set(), []
        for p in paras:
            if p not in seen:
                d.append(p); seen.add(p)
        return "\n".join(d)
    except Exception:
        return ""

def extract_pdf(path):
    if not HAS_FITZ:
        return ""
    try:
        doc = fitz.open(path)
        pages = [p.get_text("text") for p in doc]
        doc.close()
        return "\n".join(pages)
    except Exception:
        return ""

def extract_rtf(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        text = re.sub(r"\\[a-z]+\d*\s?", " ", raw)
        text = re.sub(r"[{}\\]", " ", text)
        return re.sub(r"\s+", " ", text).strip()
    except Exception:
        return ""

def extract_text(path):
    ext = Path(path).suffix.lower()
    if ext == ".docx": return extract_docx(path)
    if ext == ".pdf":  return extract_pdf(path)
    if ext == ".rtf":  return extract_rtf(path)
    return ""

# ── Name Cleanup (same as build_master_index.py) ─────────────────────────────

def get_display_name(fname):
    stem = re.sub(r"\.(docx?|pdf|rtf)$", "", fname, flags=re.I)
    for pat in [
        r"^\d{6,8}[-_\s]*", r"^\d+\s*[-–]?\s*",
        r"^KSE[-_\s]+",
        r"^(?:MASTER|Master)[_\s]+(?:Resume[_\s]+[-_\s]*)?",
        r"^[-\s]*(?:MASTER|Master)[_\s]+(?:Resume[_\s]+)?[-\s]*",
        r"^(?:Resume)\s+[-\s]*",
        r"[-_\s]+KSE\b.*$", r"[-_\s]+NJDOT\b.*$", r"[-_\s]+Master\b.*$",
        r"[-_\s]+Resume\b.*$", r"[-_\s]+Format\b.*$", r"[-_\s]+SF\s*330\b.*$",
        r"[-_\s]+Design\s*Build\b.*$", r"[-_\s]+CADD\b.*$", r"[-_\s]+CVS\b.*$",
        r"[-_\s]+TCM\b.*$", r"[-_\s]+REV\b.*$", r"[-_\s]+draft\b.*$",
        r"\s*\d{1,2}[-./]\d{1,2}[-./]\d{2,4}.*$",
        r"[-_\s]+(?:Sr|Jr|Senior|Junior|Chief|Lead|Principal)\.?\s+\w.*$",
        r"[-_\s]+(?:Inspector|Engineer|Manager|Coordinator|Analyst|Designer).*$",
        r"[-_\s]+(?:Bridge|Highway|Structural|Civil|Environmental|Quality).*$",
        r"[-_\s]+(?:Focus|Insp|OE|TL|PM|SI|CCL|NII|HM)\b.*$",
        r"[_\-\s]+$",
    ]:
        stem = re.sub(pat, "", stem, flags=re.I)
    stem = re.sub(r"[_\-]+", " ", stem).strip().strip("., ")
    return stem if len(stem) > 1 else fname

def name_key(display_name):
    return re.sub(r"\s+", "", display_name.lower())

# ── File quality scoring (prefer "Master" files, longer text) ─────────────────

def file_quality_score(fname, text_len):
    score = text_len
    fname_lower = fname.lower()
    # Prefer files explicitly named "Master"
    if "master" in fname_lower:
        score += 50_000
    # Prefer KSE format
    if "kse" in fname_lower:
        score += 20_000
    # Penalise NJDOT/SF330/QCE specialised formats (less complete)
    if "njdot" in fname_lower or "sf 330" in fname_lower or "qce" in fname_lower:
        score -= 30_000
    # Penalise "draft" versions
    if "draft" in fname_lower:
        score -= 10_000
    return score

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    all_files = sorted([
        f for f in os.listdir(RESUME_FOLDER)
        if Path(f).suffix.lower() in RESUME_EXTS
    ])
    total = len(all_files)
    print(f"\nKSE Full-Text KB Builder")
    print(f"Processing {total} resume files...\n")

    # Collect all extracted texts, keyed by person name
    person_map: dict = {}   # name_key -> {display_name, files: [(fname, text, score)]}
    no_text = []

    for i, fname in enumerate(all_files, 1):
        fpath = os.path.join(RESUME_FOLDER, fname)
        print(f"  [{i:>3}/{total}] {fname[:70]}", end="\r")

        text = extract_text(fpath)
        if not text.strip():
            no_text.append(fname)
            continue

        name = get_display_name(fname)
        key  = name_key(name)
        score = file_quality_score(fname, len(text))

        if key not in person_map:
            person_map[key] = {"display_name": name, "files": []}
        person_map[key]["files"].append((fname, text, score))

    print(" " * 80)
    print(f"\nExtracted text from {total - len(no_text)}/{total} files")
    print(f"Unique persons identified: {len(person_map)}")

    # Build final records — use best-scoring file as primary text
    records = []
    for key, entry in sorted(person_map.items(), key=lambda x: x[0]):
        # Sort files by quality score descending
        files_sorted = sorted(entry["files"], key=lambda x: x[2], reverse=True)
        primary_fname, primary_text, _ = files_sorted[0]

        # Combine text from all versions (union), primary first
        combined_parts = [primary_text]
        seen_paras = set(l.strip() for l in primary_text.splitlines() if l.strip())
        for fname, text, _ in files_sorted[1:]:
            extra = []
            for line in text.splitlines():
                ls = line.strip()
                if ls and ls not in seen_paras:
                    extra.append(ls)
                    seen_paras.add(ls)
            if extra:
                combined_parts.append("\n".join(extra))

        full_text = "\n".join(combined_parts)

        records.append({
            "display_name": entry["display_name"],
            "primary_file": primary_fname,
            "all_files": [f for f, _, _ in files_sorted],
            "char_count": len(full_text),
            "full_text": full_text,
        })

    # Write JSONL
    out_path = os.path.join(OUT_DIR, "KSE_FullText_KB.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    file_size_mb = os.path.getsize(out_path) / 1_048_576

    # Write stats
    stats_path = os.path.join(OUT_DIR, "KSE_FullText_KB_stats.txt")
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(f"KSE Full-Text KB Stats\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total persons: {len(records)}\n")
        f.write(f"File size: {file_size_mb:.1f} MB\n")
        f.write(f"Files with no text: {len(no_text)}\n\n")
        f.write(f"{'Name':<35} {'Chars':>8}  Primary File\n")
        f.write("-" * 100 + "\n")
        for rec in records:
            f.write(f"{rec['display_name'][:34]:<35} {rec['char_count']:>8}  {rec['primary_file']}\n")

    print(f"\nDone.")
    print(f"  Records : {len(records)} persons")
    print(f"  Size    : {file_size_mb:.1f} MB")
    print(f"  JSONL   : {out_path}")
    print(f"  Stats   : {stats_path}")
    if no_text:
        print(f"\n[WARN] {len(no_text)} files returned no text (image-based PDFs or corrupt):")
        for f in no_text:
            print(f"  - {f}")
    print(f"\nUpload KSE_FullText_KB.jsonl to ChatGPT for deep narrative queries.")

if __name__ == "__main__":
    main()
