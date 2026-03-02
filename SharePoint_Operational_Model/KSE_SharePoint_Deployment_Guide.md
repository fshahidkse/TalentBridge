# KS TalentBridge SharePoint Permanent Model

## Purpose
This is the permanent deterministic model for answering resume/staffing questions in ChatGPT with SharePoint `ChatGPT` site connected.

## Lists to Create (SharePoint)
Create these 4 lists in SharePoint site `ChatGPT` and import the matching CSV templates:

1. `TB_Employees` -> `SP_Employees_Template.csv`
2. `TB_Credentials` -> `SP_Credentials_Template.csv`
3. `TB_Agency_Experience` -> `SP_Agency_Experience_Template.csv`
4. `TB_Proposal_Roles` -> `SP_Proposal_Roles_Template.csv`

Optional but recommended:
5. `TB_Taxonomy_Synonyms` -> `SP_Taxonomy_Synonyms.csv`

## Column Rules (Critical)
- Treat `employee_id` as the join key across all lists.
- Keep canonical values in normalized columns:
  - `agency_name_normalized`
  - `credential_type`
  - `proposal_role`
  - `discipline`
- `evidence_quote` must be verbatim from source resume/project docs.
- `source_file_path` must point to exact file used.
- Use `active_flag` for license/cert validity; do not infer.

## Governance Workflow
1. Intake:
- Add/Update employee row in `TB_Employees`.
- Add all cert/license entries in `TB_Credentials`.
- Add agency/project evidence rows in `TB_Agency_Experience`.
- Add role-fit rows in `TB_Proposal_Roles`.

2. Verification:
- Every row must include `last_verified` and `verified_by`.
- Set `status=Active` for trusted rows, `status=Needs Review` for uncertain rows.

3. Cadence:
- Monthly refresh for high-activity teams.
- Quarterly full audit for all employees.

## Deterministic Query Pattern in ChatGPT
Use this pattern in prompts:

"First query SharePoint structured lists `TB_Employees`, `TB_Credentials`, `TB_Agency_Experience`, `TB_Proposal_Roles`. Return exact matches and evidence_quote/source_file_path. If no exact match, run one synonym pass using `TB_Taxonomy_Synonyms`, then return best matches with confidence. Return `Not found.` only if both passes have zero evidence."

## Why this works
- Structured filters answer cert/agency/role questions deterministically.
- Source quotes keep outputs audit-safe.
- Synonym pass increases recall without inventing facts.

## Seed Data (Auto-Generated)
Initial import files were generated from current resumes:
- `Seed_From_Resumes/TB_Employees_Seed.csv`
- `Seed_From_Resumes/TB_Credentials_Seed.csv`
- `Seed_From_Resumes/TB_Agency_Experience_Seed.csv`
- `Seed_From_Resumes/TB_Proposal_Roles_Seed.csv`

Import order:
1. `TB_Employees_Seed.csv`
2. `TB_Credentials_Seed.csv`
3. `TB_Agency_Experience_Seed.csv`
4. `TB_Proposal_Roles_Seed.csv`

Important:
- All seeded rows are marked `status=Needs Review` and `verified_by=AutoSeed`.
- Review and promote high-confidence rows to `status=Active`.
