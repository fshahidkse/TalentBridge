"""
search_pa_pe.py
Searches all resumes in Resume 08152025 for Pennsylvania PE license holders.
Outputs a numbered list with file name and employee name.
"""

import os, re, zipfile, json
import xml.etree.ElementTree as ET

try:
    import fitz
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

FOLDER = r"c:\Users\KSE\Desktop\TalentBridge\Resume 08152025"
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RESUME_EXTS = {".docx", ".pdf", ".rtf"}


# ── Text extraction (reused from existing scripts) ──

def extract_docx(path):
    try:
        with zipfile.ZipFile(path) as z:
            parts = ["word/document.xml"]
            parts += sorted(n for n in z.namelist() if re.match(r"word/(header|footer)", n))
            paras = []
            for part in parts:
                try:
                    with z.open(part) as f:
                        root = ET.fromstring(f.read())
                        for p in root.iter(f"{W_NS}p"):
                            t = "".join(n.text for n in p.iter(f"{W_NS}t") if n.text).strip()
                            if t:
                                paras.append(t)
                except (KeyError, ET.ParseError):
                    pass
        seen, deduped = set(), []
        for p in paras:
            if p not in seen:
                deduped.append(p); seen.add(p)
        return "\n".join(deduped)
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
    ext = path.lower().rsplit(".", 1)[-1]
    if ext == "docx": return extract_docx(path)
    if ext == "pdf":  return extract_pdf(path)
    if ext == "rtf":  return extract_rtf(path)
    return ""


# ── Name extraction from filename ──

def get_name_from_filename(fname):
    stem = re.sub(r"\.(docx|pdf|rtf)$", "", fname, flags=re.I)
    # Remove leading numbers/dates
    stem = re.sub(r"^\d{6,8}[-_\s]*", "", stem)
    stem = re.sub(r"^\d+\s*[-–]?\s*", "", stem)
    # Remove common suffixes
    noise = [
        r"[-_\s]*KSE.*$", r"[-_\s]*Resume.*$", r"[-_\s]*Master.*$",
        r"[-_\s]*Format.*$", r"[-_\s]*NJDOT.*$", r"[-_\s]*SF\s*330.*$",
        r"[-_\s]*Design\s*Build.*$", r"[-_\s]*CADD.*$", r"[-_\s]*Insp.*$",
        r"[-_\s]*CCL.*$", r"[-_\s]*TCM.*$", r"[-_\s]*CVS.*$",
        r"[-_\s]*TL\s*$", r"[-_\s]*PM\s*$", r"[-_\s]*OE\s*$",
        r"[-_\s]*REV.*$", r"[-_\s]*updated.*$", r"[-_\s]*marked.*$",
        r"\s*\d{1,2}[-./]\d{1,2}[-./]\d{2,4}.*$",
        r"[-_\s]+(?:Sr|Jr|Senior|Junior|Chief|Lead|Principal)\.?\s.*$",
        r"[-_\s]+(?:Quality|Construction|Bridge|Structural|Civil|Special).*$",
        r"[-_\s]+(?:Inspector|Engineer|Manager|Coordinator|Analyst).*$",
    ]
    for pat in noise:
        stem = re.sub(pat, "", stem, flags=re.I)
    stem = re.sub(r"[_\-]+", " ", stem).strip().strip("., ")
    return stem if stem else fname


# ── PA PE detection — exhaustive multi-variant search ──

PA_PE_PATTERNS = [
    # Direct "PA PE" or "Pennsylvania PE" patterns
    re.compile(r"P\.?E\.?\s*[-–—]?\s*(?:Pennsylvania|PA)\b", re.I),
    re.compile(r"(?:Pennsylvania|PA)\s*[-–—:,]?\s*P\.?E\.?", re.I),
    re.compile(r"(?:Pennsylvania|PA)\s+(?:Professional\s+Engineer|Licensed\s+.*Engineer)", re.I),
    re.compile(r"Professional\s+Engineer\s*[-–—:,/]?\s*(?:Pennsylvania|PA)", re.I),
    re.compile(r"Licensed\s+Professional\s+Engineer.*(?:Pennsylvania|PA)", re.I),
    re.compile(r"(?:Pennsylvania|PA)\s*(?:#|No\.?|License|Lic\.?)?\s*(?:PE|P\.E\.)", re.I),
    # License listing patterns like "NJ, NY, PA" or "PA, NJ, NY" near PE
    re.compile(r"P\.?E\.?\s*[-–—:,]?\s*(?:(?:NJ|NY|CT|DE|MD|VA|NC|OH|FL|MA)\s*[,/&]\s*)*PA\b", re.I),
    re.compile(r"P\.?E\.?\s*[-–—:,]?\s*PA\s*[,/&]", re.I),
    re.compile(r"\bPA\s*[,/&]\s*(?:(?:NJ|NY|CT|DE|MD|VA|NC|OH|FL|MA)\s*[,/&]\s*)*.*P\.?E\.?", re.I),
    # State listing with PA included near PE context
    re.compile(r"(?:Registered|Licensed)\s+(?:in|:)\s*.*\bPA\b", re.I),
    # PE license number patterns
    re.compile(r"(?:PA|Pennsylvania)\s*(?:PE|P\.E\.)\s*#?\s*\d{4,6}", re.I),
    re.compile(r"PE\s*#?\s*\d{4,6}\s*[-–—,]?\s*(?:PA|Pennsylvania)", re.I),
]

# Context patterns: lines mentioning PE that also mention PA somewhere nearby
PE_LINE_RE = re.compile(r"\bP\.?E\.?\b", re.I)
PA_CONTEXT_RE = re.compile(r"\b(?:Pennsylvania|PA)\b", re.I)


def check_pa_pe(full_text):
    """Returns (is_match, evidence_lines) for PA PE license."""
    evidence = []

    # Pattern 1: Direct regex matches
    for pat in PA_PE_PATTERNS:
        for m in pat.finditer(full_text):
            start = max(0, m.start() - 60)
            end = min(len(full_text), m.end() + 60)
            snippet = full_text[start:end].replace("\n", " ").strip()
            evidence.append(snippet)

    # Pattern 2: Line-by-line — find lines with PE that have PA within ±3 lines
    lines = full_text.splitlines()
    for i, line in enumerate(lines):
        if PE_LINE_RE.search(line):
            window = "\n".join(lines[max(0, i-3):i+4])
            if PA_CONTEXT_RE.search(window):
                snippet = line.strip()
                if snippet and len(snippet) > 5:
                    evidence.append(snippet)

    # Deduplicate evidence
    seen = set()
    unique_evidence = []
    for e in evidence:
        e_clean = e[:120]
        if e_clean not in seen:
            seen.add(e_clean)
            unique_evidence.append(e_clean)

    return len(unique_evidence) > 0, unique_evidence[:5]


# ── Main search ──

def main():
    all_files = sorted([
        f for f in os.listdir(FOLDER)
        if os.path.splitext(f)[1].lower() in RESUME_EXTS
    ])
    total = len(all_files)
    print(f"Scanning {total} resume files for PA PE license holders...\n")

    results = []
    errors = []

    for i, fname in enumerate(all_files, 1):
        fpath = os.path.join(FOLDER, fname)
        print(f"  [{i:>3}/{total}] {fname[:65]}", end="\r")

        text = extract_text(fpath)
        if not text:
            errors.append(fname)
            continue

        is_match, evidence = check_pa_pe(text)
        if is_match:
            name = get_name_from_filename(fname)
            results.append({
                "name": name,
                "file": fname,
                "evidence": evidence
            })

    # Output
    print(" " * 80)
    print(f"\n{'='*70}")
    print(f"PA PE LICENSE HOLDERS FOUND: {len(results)}")
    print(f"{'='*70}\n")

    for idx, r in enumerate(results, 1):
        print(f"{idx:>3}. {r['name']}")
        print(f"     File: {r['file']}")
        print(f"     Evidence: \"{r['evidence'][0]}\"")
        if len(r['evidence']) > 1:
            for e in r['evidence'][1:3]:
                print(f"               \"{e}\"")
        print()

    if errors:
        print(f"\n[WARN] {len(errors)} files could not be read (empty/corrupt)")

    # Also save as JSON for reference
    out_path = os.path.join(FOLDER, "_PA_PE_Search_Results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"total_found": len(results), "results": results}, f, indent=2, ensure_ascii=False)
    print(f"\nResults also saved to: {out_path}")


if __name__ == "__main__":
    main()
