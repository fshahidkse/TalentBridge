# KS TalentBridge

AI-powered staffing and proposal search tool for KS Engineers (350-person AEC firm, Newark NJ).

## What It Does

- **Staff lookup**: Find staff by license (PE, EIT), certification (NICET, ACI, OSHA-30, PMP, etc.), agency experience, discipline, and leadership role
- **Proposal staffing**: Build candidate lists for any project type, agency, and role combination
- **Resume search**: Full-text search across 274 staff records
- **Compliance matrices**: Verify credentials against project requirements

## Architecture

```
TalentBridge/
├── data/
│   ├── index/              ← Layer 1: Structured CSV index (274 staff × 201 columns)
│   │   └── archive/        ← v1 index and backups
│   ├── kb/                 ← Layer 2: Full-text knowledge base (JSONL + MD)
│   └── source/             ← Source documents
│       ├── Resume 08152025/        (297 resume files — DOCX/PDF/RTF)
│       ├── Completed PDS 09082025/ (project data sheets)
│       └── Incomplete PDS 09172025/
├── scripts/                ← Python builders and search tools
│   └── archive/            ← Older scripts (superseded)
├── prompts/                ← System prompts for ChatGPT / Claude
│   └── archive/
├── docs/                   ← Documentation, benchmarks, sample queries
└── outputs/                ← Generated reports and stats
```

## Quick Start

### Rebuild the index (after adding/updating resumes)
```bash
python scripts/build_master_index_v2.py   # → data/index/KSE_Master_Index_v2.csv + .xlsx
python scripts/build_fulltext_kb.py       # → data/kb/KSE_FullText_KB.jsonl + .md
```

### Run a search (in Claude Code)
Just ask a question in this chat. Claude reads the local CSV and JSONL directly.

### Deploy to ChatGPT Teams
1. Upload `data/index/KSE_Master_Index_v2.csv` to GPT Knowledge
2. Upload `data/kb/KSE_FullText_KB.md` to GPT Knowledge
3. Copy system prompt from `prompts/System Prompt v4.md` into the GPT instructions
4. Add SharePoint connector pointing at `data/source/Resume 08152025/`

## Dependencies

```bash
pip install -r requirements.txt
```

## Data Coverage

| Layer | File | Coverage |
|---|---|---|
| Index (Layer 1) | `KSE_Master_Index_v2.csv` | 274 staff, 201 columns |
| Full text (Layer 2) | `KSE_FullText_KB.jsonl` / `.md` | 273 persons, 4.8 MB |
| Resumes | `Resume 08152025/` | 297 files (DOCX/PDF/RTF) |
