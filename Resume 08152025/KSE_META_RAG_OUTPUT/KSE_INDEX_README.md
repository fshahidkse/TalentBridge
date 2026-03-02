# KSE Index README

## What this is
- High-recall resume metadata index for proposal staffing and semantic search preparation.
- One row per resume (one person record per file).
- Designed to maximize discoverability; false positives are tolerated to avoid misses.

## Files generated
- KSE_RESUME_INDEX.csv
- KSE_RESUME_INDEX.xlsx
- KSE_SYNONYMS.md
- KSE_INDEX_README.md

## Source and run context
- Input folder: `C:\Users\KSE\Desktop\TalentBridge\Resume 08152025`
- Output folder: `C:\Users\KSE\Desktop\TalentBridge\Resume 08152025\KSE_META_RAG_OUTPUT`
- Records generated: `297`
- Generated on: `2026-02-27 14:34:22`

## How to run
```bash
python build_kse_resume_index.py --input "PATH_TO_RESUME_FOLDER" --output "OUTPUT_FOLDER"
```

## Update process
1. Add new resumes to the input folder.
2. Re-run the script with the same output folder.
3. Review quality_flags for parse issues and scanned PDFs.
4. Review KSE_SYNONYMS.md and add new domain variants as needed.

## Behavior notes
- agencies_tags include explicit agency mentions plus helper variants where appropriate.
- evidence_snippets are verbatim short lines from resumes (<=200 chars each).
- If person_name cannot be confidently identified, person_name is Unknown.
- SCANNED_PDF? indicates weak extraction likely from image-based PDF.
