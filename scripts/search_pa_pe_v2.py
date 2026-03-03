"""
search_pa_pe_v2.py
Exhaustive global search — PA PE license holders.
Casts the widest possible net with all known formatting variants.
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

# ── Text extraction ──────────────────────────────────────────────────────────

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
                            if t: paras.append(t)
                except: pass
        seen, d = set(), []
        for p in paras:
            if p not in seen: d.append(p); seen.add(p)
        return "\n".join(d)
    except: return ""

def extract_pdf(path):
    if not HAS_FITZ: return ""
    try:
        doc = fitz.open(path)
        pages = [p.get_text("text") for p in doc]
        doc.close()
        return "\n".join(pages)
    except: return ""

def extract_rtf(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        text = re.sub(r"\\[a-z]+\d*\s?", " ", raw)
        text = re.sub(r"[{}\\]", " ", text)
        return re.sub(r"\s+", " ", text).strip()
    except: return ""

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx": return extract_docx(path)
    if ext == ".pdf":  return extract_pdf(path)
    if ext == ".rtf":  return extract_rtf(path)
    return ""

# ── Name from filename ────────────────────────────────────────────────────────

def get_name(fname):
    stem = re.sub(r"\.(docx|pdf|rtf)$", "", fname, flags=re.I)
    for pat in [
        r"[-_\s]*KSE.*$", r"[-_\s]*NJDOT.*$", r"[-_\s]*Master.*$",
        r"[-_\s]*Resume.*$", r"[-_\s]*Format.*$", r"[-_\s]*SF\s*330.*$",
        r"[-_\s]*Design.*$", r"[-_\s]*CADD.*$", r"[-_\s]*CVS.*$",
        r"[-_\s]*TCM.*$", r"[-_\s]*PM\s*$", r"[-_\s]*TL\s*$",
        r"[-_\s]*REV.*$", r"[-_\s]*draft.*$", r"[-_\s]*copy.*$",
        r"\s*\d{1,2}[-./]\d{1,2}[-./]\d{2,4}.*$",
        r"^\d+\s*[-–]?\s*", r"^\d{6,8}[-_\s]*",
        r"[-_\s]+(?:Sr|Jr|Senior|Junior|Chief|Lead|Principal)\.?\s.*$",
        r"[-_\s]+(?:Inspector|Engineer|Manager|Coordinator|Analyst).*$",
    ]:
        stem = re.sub(pat, "", stem, flags=re.I)
    stem = re.sub(r"[_\-]+", " ", stem).strip().strip("., ")
    return stem if stem else fname

# ── EXHAUSTIVE PA PE PATTERNS ─────────────────────────────────────────────────
#
# Group A: Explicit "PA" + "PE" or "Professional Engineer" on same line/nearby
# Group B: State listing patterns that include PA with PE context
# Group C: License number formats
# Group D: Prose descriptions
# Group E: Multi-state listing where PA appears alongside other states near PE

PA_PE_DIRECT = [
    # "Professional Engineer/PA", "Professional Engineer - PA", "Professional Engineer PA"
    re.compile(r"Professional\s+Engineer\s*[/\-–—:,]?\s*PA\b", re.I),
    re.compile(r"Professional\s+Engineer[^.\n]{0,60}Pennsylvania", re.I),
    re.compile(r"Pennsylvania[^.\n]{0,60}Professional\s+Engineer", re.I),
    re.compile(r"Licensed\s+Professional\s+Engineer[^.\n]{0,80}Pennsylvania", re.I),
    re.compile(r"Licensed\s+Professional\s+Engineer[^.\n]{0,80}\bPA\b", re.I),
    re.compile(r"Pennsylvania[^.\n]{0,80}Licensed\s+Professional\s+Engineer", re.I),
    re.compile(r"Registered\s+Professional\s+Engineer[^.\n]{0,80}Pennsylvania", re.I),
    re.compile(r"Registered\s+Professional\s+Engineer[^.\n]{0,80}\bPA\b", re.I),
    # "PE - PA", "PE/PA", "P.E. PA", "P.E./PA"
    re.compile(r"\bP\.?E\.?\s*[/\-–—]\s*PA\b", re.I),
    re.compile(r"\bPA\s*[/\-–—]\s*P\.?E\.?\b", re.I),
    re.compile(r"\bPE\s+PA\b"),
    re.compile(r"\bPA\s+PE\b"),
    re.compile(r"\bPA\s*\(?P\.?E\.?\b", re.I),
    # "Pennsylvania #PE", "Pennsylvania PE", "Pennsylvania P.E."
    re.compile(r"Pennsylvania\s+(?:#\s*)?P\.?E\.?\b", re.I),
    re.compile(r"P\.?E\.?\s+Pennsylvania", re.I),
    # "PA (License No.", "PA (PE", "PA (#PE"
    re.compile(r"\bPA\s*\((?:#\s*)?(?:PE|P\.E\.|License|Lic\.?|No\.?)", re.I),
    re.compile(r"\bPA\s*(?:#|No\.?)?\s*PE\s*\d{4,6}", re.I),
    # License number formats: "PE040060E", "PE078118", "PE053056"
    re.compile(r"\bPA\b[^.\n]{0,30}PE\d{4,6}[A-Z]?\b"),
    re.compile(r"\bPE\d{4,6}[A-Z]?\b[^.\n]{0,30}\bPA\b"),
    re.compile(r"#PE\d{4,6}"),
    # "PE PA #", "PE PA (", "(PA #", "(PA, #PE"
    re.compile(r"PE\s+PA\s*[#(]", re.I),
]

# State listing patterns — PE appears near a list that includes PA
# e.g. "NJ, NY, & PA", "NY, NJ, PA", "PA, NJ, NY", etc.
STATE_LIST_WITH_PA = [
    re.compile(r"P\.?E\.?[^.\n]{0,80}(?:NJ|NY|CT|MD|VA|DE|FL|NC|MA)[^.\n]{0,20}\bPA\b", re.I),
    re.compile(r"P\.?E\.?[^.\n]{0,80}\bPA\b[^.\n]{0,20}(?:NJ|NY|CT|MD|VA|DE|FL|NC|MA)", re.I),
    re.compile(r"\bPA\b[^.\n]{0,20}(?:NJ|NY|CT|MD|VA|DE|FL|NC|MA)[^.\n]{0,80}P\.?E\.?", re.I),
    re.compile(r"(?:NJ|NY|CT|MD|VA|DE)[^.\n]{0,20}\bPA\b[^.\n]{0,80}P\.?E\.?", re.I),
    # "in PA, NJ and NY" near "engineer"
    re.compile(r"(?:licensed|registered|professional)\s+(?:in|engineer)[^.\n]{0,80}\bPA\b", re.I),
    re.compile(r"\bPA\b[^.\n]{0,80}(?:licensed|registered)\s+(?:professional\s+)?engineer", re.I),
]

# Prose variants
PROSE_PA_PE = [
    re.compile(r"PE\s+in\s+(?:the\s+state\s+of\s+)?(?:Pennsylvania|PA)\b", re.I),
    re.compile(r"(?:Pennsylvania|PA)\s+PE\s+license", re.I),
    re.compile(r"licensed\s+in\s+Pennsylvania", re.I),
    re.compile(r"registered\s+in\s+Pennsylvania", re.I),
    re.compile(r"Pennsylvania\s+(?:state\s+)?(?:PE|P\.E\.|Professional\s+Engineer)\s+(?:license|no|#|registration)", re.I),
    re.compile(r"(?:PE|P\.E\.)\s+license[^.\n]{0,40}Pennsylvania", re.I),
    re.compile(r"P\.?E\.?\s*in\s+(?:PA|Pennsylvania)\b", re.I),
    re.compile(r"(?:PA|Pennsylvania)\s+(?:state\s+)?P\.?E\.?\s*(?:license|#|no\.?|registration)?", re.I),
    re.compile(r"P\.?E\.?\s*,?\s*PA\s*\(", re.I),
    re.compile(r"\bexp(?:ires?|\.)\s*\d+[/.\-]\d+[/.\-]?\d*[^.\n]{0,30}PA\b", re.I),
]

ALL_PATTERNS = PA_PE_DIRECT + STATE_LIST_WITH_PA + PROSE_PA_PE

# Hard false-positive filters — lines matching these are skipped
FALSE_POS = re.compile(
    r"paper(?:work|s?\b)|"
    r"\bPAPAR\b|"
    r"pave?ment|"
    r"PAPA\b|"
    r"PANYNJ|"
    r"PATCO|"
    r"PAX\b|"
    r"PARCEL|"
    r"parade|"
    r"\bpa\s+approach\b|"           # "PA approach spans"
    r"king\s+of\s+prussia\b|"       # city name only
    r"(?:camp|smith|nps|park)\s*,?\s*pa\b",  # location-only
    re.I
)

# Also exclude lines that are clearly just project location mentions
# (city, PA without any PE/engineer/license context)
LOCATION_ONLY = re.compile(
    r"^[^P]*(?:philadelphia|pittsburgh|harrisburg|allentown|scranton|"
    r"king of prussia|bethlehem|easton|camden|trenton)[^P]*,\s*pa[^E]*$",
    re.I
)


def is_false_positive(snippet):
    if FALSE_POS.search(snippet):
        return True
    if LOCATION_ONLY.search(snippet):
        return True
    # If the only "PA" match is inside PANYNJ, PATCO, etc.
    clean = re.sub(r"PANYNJ|PATCO|PARHTA|PARPA|PAACM", "", snippet, flags=re.I)
    return False


def check_pa_pe(full_text):
    """Returns (is_match, evidence_lines)"""
    evidence = []
    lines = full_text.splitlines()

    # Line-by-line search with all patterns
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped or len(line_stripped) < 4:
            continue

        # Test each pattern
        for pat in ALL_PATTERNS:
            if pat.search(line_stripped):
                if not is_false_positive(line_stripped):
                    # Get a small window of context
                    window = " | ".join(
                        l.strip() for l in lines[max(0,i-1):i+2] if l.strip()
                    )
                    evidence.append(line_stripped[:200])
                break  # one pattern match per line is enough

    # Deduplicate
    seen, unique = set(), []
    for e in evidence:
        key = e[:100].lower()
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return len(unique) > 0, unique[:8]


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    all_files = sorted([
        f for f in os.listdir(FOLDER)
        if os.path.splitext(f)[1].lower() in RESUME_EXTS
    ])
    total = len(all_files)
    print(f"Exhaustive PA PE search across {total} files...\n")

    results = []
    no_text = []

    for i, fname in enumerate(all_files, 1):
        fpath = os.path.join(FOLDER, fname)
        print(f"  [{i:>3}/{total}] {fname[:65]}", end="\r")

        text = extract_text(fpath)
        if not text.strip():
            no_text.append(fname)
            continue

        matched, evidence = check_pa_pe(text)
        if matched:
            results.append({
                "name": get_name(fname),
                "file": fname,
                "evidence": evidence
            })

    # ── Deduplicate by person name ─────────────────────────────────────────
    # Multiple resume versions of same person — keep all files but group
    name_map = {}
    for r in results:
        key = re.sub(r"\s+", "", r["name"].lower())
        if key not in name_map:
            name_map[key] = []
        name_map[key].append(r)

    print(" " * 80)
    print(f"\n{'='*70}")
    print(f"PA PE LICENSE HOLDERS — EXHAUSTIVE SEARCH RESULTS")
    print(f"Raw file hits: {len(results)} | Unique persons: {len(name_map)}")
    print(f"{'='*70}\n")

    idx = 1
    for key, entries in sorted(name_map.items(), key=lambda x: x[0]):
        # Use the entry with the most evidence
        best = max(entries, key=lambda e: len(e["evidence"]))
        print(f"{idx:>3}. {best['name']}")
        for e in best["evidence"][:3]:
            safe = e[:150].encode("ascii", errors="replace").decode("ascii")
            print(f"       >> \"{safe}\"")
        if len(entries) > 1:
            dupes = [e["file"] for e in entries if e["file"] != best["file"]]
            print(f"       [Also found in: {', '.join(dupes[:3])}]")
        print()
        idx += 1

    if no_text:
        print(f"\n[WARN] {len(no_text)} files returned no text (possibly image-based PDFs or corrupt)")

    # Save JSON
    out_path = os.path.join(FOLDER, "_PA_PE_Search_v2.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "raw_file_hits": len(results),
            "unique_persons": len(name_map),
            "results": [max(v, key=lambda e: len(e["evidence"])) for v in name_map.values()]
        }, f, indent=2, ensure_ascii=False)
    print(f"\nSaved -> {out_path}")

if __name__ == "__main__":
    main()
