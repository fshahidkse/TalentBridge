# Resume Deterministic Query Protocol

Use this when querying resume/employee data in ChatGPT with Code Interpreter.

## 1) Upload these files

- `Resume 08152025/Deterministic_Resume_Pack/TB_staff.parquet`
- `Resume 08152025/Deterministic_Resume_Pack/TB_resume_facts.parquet`
- `Resume 08152025/Deterministic_Resume_Pack/TB_chunks.parquet`

## 2) Paste this instruction block before each query

```text
Use Python/pandas only. Do not infer missing facts.
Load TB_staff.parquet, TB_resume_facts.parquet, TB_chunks.parquet.
For filtering, use exact fact_key/fact_type matches.
Return deterministic output sorted by person_name ASC.
Always include: person_name, source_file, evidence_snippet.
If no rows match, return exactly: Not found.
```

## 3) Canonical fact keys

### Credentials (`fact_type = credential`)
- `PE_LICENSE_STATE` (qualifier includes state code such as `PA`, `NJ`)
- `PE_LICENSE_NUMBER`
- `PENNDOT_RCI` (qualifier can include `LEVEL_1`, `LEVEL_2`, etc.)
- `PENNDOT_TCI`
- `NICET`
- `NICET_CMT`
- `OSHA_10`
- `OSHA_30`
- `NACE_COATING`
- `PP_LICENSE_NJ`
- `CFM`

### Agencies (`fact_type = agency`)
- `NJDOT`, `PENNDOT`, `NYSDOT`, `NJ_TRANSIT`, `PANYNJ`, `SEPTA`, `AMTRAK`
- `PHILA_STREETS`, `DELDOT`, `FAA`, `DRPA`, `NJDEP`, `USACE`, `NEWARK`, `TURNPIKE`

### Disciplines (`fact_type = discipline`)
- `BRIDGE_DESIGN`, `BRIDGE_INSPECTION`, `HIGHWAY_DESIGN`, `TRAFFIC_SIGNAL`
- `HYDRO_HYDRAULICS`, `CM_CI`, `GEOTECH`, `ENV_PERMITTING`
- `STEEL_REHAB`, `COATING_QAQC`, `UTILITY_COORD`

### Roles (`fact_type = role`)
- `PROJECT_MANAGER`, `RESIDENT_ENGINEER`, `CHIEF_INSPECTOR`, `LEAD_DESIGNER`, `QAQC_LEAD`

## 4) Example deterministic filters

### Who has a PA PE license?

```python
result = facts[
    (facts["fact_type"] == "credential") &
    (facts["fact_key"] == "PE_LICENSE_STATE") &
    (facts["qualifier"] == "PA")
][["person_name", "file_name", "evidence_snippet"]].drop_duplicates().sort_values("person_name")
```

### Who has NJDOT experience?

```python
result = facts[
    (facts["fact_type"] == "agency") &
    (facts["fact_key"] == "NJDOT")
][["person_name", "file_name", "evidence_snippet"]].drop_duplicates().sort_values("person_name")
```

### Who has OSHA 10 or OSHA 30?

```python
result = facts[
    (facts["fact_type"] == "credential") &
    (facts["fact_key"].isin(["OSHA_10", "OSHA_30"]))
][["person_name", "fact_key", "file_name", "evidence_snippet"]].drop_duplicates().sort_values(["person_name", "fact_key"])
```

