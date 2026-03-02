# KS Resume Query -> SharePoint Filter Map

## Certification / Credential
1. PennDOT RCI Level 1/2/3
- List: `TB_Credentials`
- Filters: `credential_type='PennDOT RCI'` + `level in {1,2,3}` + `active_flag=true`

2. NICET Construction Materials Testing
- List: `TB_Credentials`
- Filters: `credential_type='NICET'` + `credential_name contains 'Construction Materials'`

3. PE in NJ / PE in PA
- List: `TB_Credentials`
- Filters: `credential_type='Professional Engineer'` + `state='NJ' or 'PA'`

4. PP in NJ / CFM / NACE L1-L3 / OSHA 10 or 30
- List: `TB_Credentials`
- Filters by `credential_type`, `state`, `level`

## DOT / Agency Experience
- List: `TB_Agency_Experience`
- Filters by `agency_name_normalized`:
  - NJDOT, PennDOT, NYSDOT, NJ Transit, PANYNJ, SEPTA, Amtrak, DelDOT, FAA, DRPA, NJDEP, USACE

## Discipline Questions
- List: `TB_Agency_Experience`
- Filter `discipline` + `project_type`
  - bridge design, bridge inspection, traffic, hydrology/hydraulics, geotech, CM/CI, environmental permitting, steel rehab, coating QA/QC

## Leadership / Proposal Roles
- List: `TB_Proposal_Roles`
- Filters:
  - `proposal_role` in (Project Manager, Resident Engineer, Chief Inspector, QA/QC Lead, Lead Designer)
  - optionally `agency_context` and `discipline_context`

## Join Pattern
- Start with filtered IDs from one list.
- Join to `TB_Employees` on `employee_id`.
- Return: `full_name`, relevant fields, `evidence_quote`, `source_file_path`, `last_verified`.

## Return Policy
- Exact pass first.
- Synonym/helper pass second via `TB_Taxonomy_Synonyms`.
- `Not found.` only after both passes fail.
