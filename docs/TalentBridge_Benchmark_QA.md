# KS TalentBridge — Benchmark Q&A (Verified Ground Truth)

**Purpose:** Use these questions and answers to validate KS TalentBridge (ChatGPT Teams + SharePoint).
Each answer was verified by directly scanning all 301 resume files in `Resume 08152025\`.
Any AI system querying this database should match these results.

**Data Sources:**
- Layer 1: `KSE_Master_Index.csv` (274 staff, 148 columns)
- Layer 2: `KSE_FullText_KB.jsonl` (273 persons, full resume text)
- Resume Folder: `Resume 08152025\` (301 files, 274 unique staff)

---

## Q1 — Pennsylvania (PA) Professional Engineer License

**Question:** Who at KS Engineers holds a Pennsylvania Professional Engineer (PE) license? List each person's name and PA PE license number.

**Expected Answer:** 23 confirmed PA PE holders (includes active and expired licenses)

| # | Name | PA PE Number | Status |
|---|------|-------------|--------|
| 1 | Fitzgerald, G. | PE053056 | Active |
| 2 | Jacurak, Adam | PE080204 | Active |
| 3 | Burrell, R. | PE078118 | Active |
| 4 | Mikaeel, M. | PE083968 | Active |
| 5 | Sheppard, J. | PE096834 | Active |
| 6 | Scancella, R. | PE042838R | Active |
| 7 | Zarriello, J. | PE027442E | Active |
| 8 | Cooke, Nicholas | PE094773 | Active |
| 9 | Abdalla Ashraf, M. | PE054792E | Active (exp. 4/30/2026) |
| 10 | Alaimo, D. | PE028092E | Active (exp. 9/30/2025) |
| 11 | Khan, Uneeq | PE094950 | Active (exp. 4/30/2026) |
| 12 | Meidhof, C. | PE053254E | Active |
| 13 | Fox, H. | PE083389 | Active |
| 14 | Shahangian, M. | PE037732 | Active |
| 15 | Brudi, W. | Multi-state (PA included) | Active |
| 16 | Quinit, D. | Multi-state (PA included) | Active |
| 17 | Lombardo, R. | Multi-state (NJ/NY/PA) | Active |
| 18 | Skierski, S. | PE070673 | Expired |
| 19 | Whitty, J. | PE040060E | Expired |
| 20 | Frega, F. | PE041605R | Expired |
| 21 | Douglas, B. | PE048478R | Expired |
| 22 | Broberg, G. | PE032029E | Expired |
| 23 | Ullikashi, P. | PE084003 | Expired |

**Verification Notes:**
- Source: `Resume 08152025\_PA_PE_Search_v2.json` (exhaustive scan)
- Expired licenses are still listed — some holders may have since renewed
- Multi-state holders (Brudi, Quinit, Lombardo) were confirmed via resume text; PA PE number not explicitly extracted in all cases

---

## Q2 — PMP Certification

**Question:** Who at KS Engineers holds a PMP (Project Management Professional) certification?

**Expected Answer:** 3 confirmed PMP holders

| # | Name | Notes |
|---|------|-------|
| 1 | Frega, F. | Confirmed PMP certification |
| 2 | Elsissi, Hatem | Confirmed PMP certification |
| 3 | Stravchinsky, Lev | Confirmed PMP certification |

**Verification Notes:**
- FALSE POSITIVES to watch for (these should NOT be returned):
  - **Sedholm, K.** — resume mentions PMP preparation/study, not active certification
  - **Marlon Plaza** — resume mentions PMP coursework, not active certification
  - **Sprau, R.** — resume references a colleague's PMP, not personal certification
  - **Abdalla Ashraf, M.** — "PMP" appears as a document/project acronym, not a personal certification
- A correct system should return exactly 3 names, not 7 or 8.

---

## Q3 — CCM Certification

**Question:** Who at KS Engineers holds a CCM (Certified Construction Manager) certification?

**Expected Answer:** 3 confirmed CCM holders

| # | Name | Notes |
|---|------|-------|
| 1 | Abdalla Ashraf, M. | Confirmed CCM certification |
| 2 | Sanigepalli, Srinivas | Confirmed CCM certification |
| 3 | Sprau, R. | Confirmed CCM certification |

**Verification Notes:**
- FALSE POSITIVES to watch for:
  - **D. Nieto / Nieto, D.** — "CCM" appears as a project team name (Construction Controls Manager), not a personal certification
  - **Ali Syed** — "CCM" used as a project/team acronym, not personal certification
  - **Taveras, Jose M.** — "CCM" used as a project team acronym
- A correct system should return exactly 3 names, not 6 or 7.

---

## Q4 — SEPTA Experience

**Question:** Which KS Engineers staff have experience working on SEPTA (Southeastern Pennsylvania Transportation Authority) projects?

**Expected Answer:** 16 unique staff with confirmed SEPTA experience

| # | Name |
|---|------|
| 1 | Alford Leon |
| 2 | Bocchinfuso, S. |
| 3 | Carola, C. |
| 4 | Cichon, Wojciech |
| 5 | Cuffee, M. |
| 6 | Douglas, B. |
| 7 | Harris Salahuddin, N. |
| 8 | Kern, L. |
| 9 | Krasucki, K. |
| 10 | Mere Barrera, A. |
| 11 | Perlmutter, J. |
| 12 | Rupnarain, D. |
| 13 | Scancella, R. |
| 14 | Tylutki, B. |
| 15 | Velasquez, L. |
| 16 | Zarriello, J. |

---

## Q5 — NICET Construction Materials Testing (CMT)

**Question:** Who at KS Engineers holds a NICET certification in Construction Materials Testing (CMT)?

**Expected Answer:** Not found — 0 staff hold this specialty

| # | Result |
|---|--------|
| 1 | Not found |

**Verification Notes:**
- KS Engineers has extensive NICET certifications, but all are in **Highway Construction (Inspection)** specialty — not Construction Materials Testing.
- A correct system should return "Not found" or "0 results," not confuse NICET Highway with NICET CMT.
- See Q9 for the full list of NICET-certified staff (all in Highway Construction specialty).

---

## Q6 — Fracture Critical Bridge Inspection

**Question:** Which KS Engineers staff have Fracture Critical bridge inspection experience?

**Expected Answer:** 13 unique staff with confirmed Fracture Critical experience

| # | Name |
|---|------|
| 1 | Assis, George |
| 2 | Brown, R. |
| 3 | Ferrante, Joseph |
| 4 | Fitzgerald, G. |
| 5 | Gilardi, A. |
| 6 | Perlmutter, J. |
| 7 | Pola, S. |
| 8 | Sedycias, D. |
| 9 | Saul Rolston |
| 10 | Shah, C. |
| 11 | Shahid, K. |
| 12 | Chet (TP-615 assignment) |
| 13 | Zarriello, J. |

---

## Q7 — PennDOT Roadway Construction Inspection Level 1

**Question:** Who at KS Engineers holds PennDOT Roadway Construction Inspection (RCI) Level 1 certification?

**Expected Answer:** 0 exact matches under that title; 2 staff hold the equivalent credential

| # | Name | Credential |
|---|------|-----------|
| — | No exact "PennDOT RCI Level 1" matches found | — |
| 1 | Herrmann, J. | PennDOT TA-TCI (equivalent program) |
| 2 | Diaz Blanco, P. | PennDOT TA-TCI (equivalent program) |

**Verification Notes:**
- PennDOT uses the "TA-TCI" (Transportation Academy — Transportation Construction Inspector) program across 13 modules — this is the standard PennDOT inspection credential equivalent to "RCI Level 1."
- A correct system should note 0 exact RCI-L1 matches but surface the TA-TCI equivalents.

---

## Q8 — NHI Course 130055 (Safety Inspection of In-Service Bridges)

**Question:** Who at KS Engineers has completed NHI Course 130055 (Safety Inspection of In-Service Bridges)?

**Expected Answer:** 20 unique staff with confirmed NHI 130055 completion

| # | Name |
|---|------|
| 1 | Baez, I. |
| 2 | Brown, R. |
| 3 | Chet (TP-615) |
| 4 | Ferrante, Joseph |
| 5 | Grandhi, V. |
| 6 | Islam, R. |
| 7 | Jacurak, Adam |
| 8 | Junaid Syed |
| 9 | Juttukonda, A. |
| 10 | J. Pena (Senior Culvert Inspector) |
| 11 | Morais, E. |
| 12 | Perlmutter, J. |
| 13 | Pola, S. |
| 14 | Quinit, D. |
| 15 | Ravalika Katta |
| 16 | Saul Rolston |
| 17 | Sedycias, D. |
| 18 | Shahid, K. |
| 19 | Sotomayor, D. |
| 20 | Zarriello, J. |

**Verification Notes:**
- FALSE POSITIVES to watch for:
  - **Molison, S.** — holds NHI **130091** (not 130055); the index may flag this as 130055
  - **Shah, C.** — NHI 130055 not confirmed in resume text; remove if system returns this name
- A correct system should return 20 names, not 22+.

---

## Q9 — NICET Certified Staff (All Specialties / All Levels)

**Question:** Who at KS Engineers holds a NICET certification (any specialty, any level)?

**Expected Answer:** 27 unique NICET-certified staff

| # | Name | NICET Level / Specialty |
|---|------|------------------------|
| 1 | Al-Jamal, J. | Level IV (multiple specialties) |
| 2 | Assis, George | NICET certified |
| 3 | Bibaoui, R. | NICET certified |
| 4 | Boris Vays | NICET certified |
| 5 | Burrell, R. | NICET certified |
| 6 | Carola, C. | NICET certified |
| 7 | Carrasquillo, J. | Water-Based Fire Protection Systems, Level III |
| 8 | Castillo, E. | Level IV |
| 9 | Christopher Hanna | NICET certified |
| 10 | Chelsey Cooke | NICET certified |
| 11 | Esquilin, L. | Level II |
| 12 | Gilardi, A. | Level I |
| 13 | Halcrow, J. | Level IV |
| 14 | Herrmann, J. | Level IV |
| 15 | Johnny Zapata | Level II |
| 16 | Taveras, Jose M. | NICET certified |
| 17 | Karatela, M. | Level I |
| 18 | Lech, D. | Level III |
| 19 | Molison, S. | Level IV |
| 20 | Okechukwu, F. | NICET certified |
| 21 | Patel, A. | Level I |
| 22 | Peaney, J. | Level III |
| 23 | Ramin Jami | NICET certified |
| 24 | Sheth, R. | Level IV |
| 25 | Skierski, S. | NICET certified |
| 26 | Trumpf, G. | Levels I, II, and III |
| 27 | Villarama, V. | Level III |

---

## Q10 — NACE Coating Inspection Certification

**Question:** Who at KS Engineers holds a NACE (National Association of Corrosion Engineers) coating inspection certification?

**Expected Answer:** 11 unique NACE-certified staff

| # | Name | NACE Level |
|---|------|-----------|
| 1 | Ahmed Zubair | Level III |
| 2 | Baez, I. | Level 1 |
| 3 | Bibaoui, R. | Level 1 |
| 4 | Cuffee, M. | NACE certified |
| 5 | Esquilin, L. | Level 2 |
| 6 | Garcia, H. | Level II |
| 7 | Gilardi, A. | Level 1 |
| 8 | Ibe, C. | Level 1 |
| 9 | Kavaleuskaya, N. | Level 1 |
| 10 | Peaney, J. | Level I |
| 11 | Ye Jackie | Level 1 |

**Verification Notes:**
- FALSE POSITIVES to watch for:
  - **Assis, George** — "NACE" appears in project/work context, not as a personal certification
  - **Saul Rolston** — "NACE" appears in project context, not as a personal certification
- A correct system should return 11 names, not 13.

---

## How to Use This Document

1. **Run each question** in your target AI system (ChatGPT Teams + SharePoint, or other).
2. **Compare results** against the expected answer table above.
3. **Flag discrepancies** — pay special attention to:
   - Missing persons (recall failures)
   - Extra persons / false positives (hallucinations or mismatches)
   - Incorrect license/certification levels
4. **Score the system:**
   - ✅ Exact match = Full credit
   - ⚠️ Missing 1-2 names = Partial credit (recall issue)
   - ❌ False positives present = Precision failure
   - ❌ Wrong count = Structural issue

---

*Generated: 2026-03-03*
*Source: KS TalentBridge, Resume 08152025 (301 files, 274 unique staff)*
*Verification method: Direct resume scan via build_fulltext_kb.py + manual review*
