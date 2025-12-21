Anonymized Enriched RWE Dataset (CSV files)

Files:
- criteria.txt : inclusion/exclusion criteria used to label patients.
- manifest.csv : one row per patient, with file names and eligibility label.
- <PATIENT_ID>_anamnesis.csv : structured outpatient note (includes narrative_note).
- <PATIENT_ID>_blood_labs.csv : longitudinal blood lab results including index-date HbA1c and eGFR.
- <PATIENT_ID>_urinalysis.csv : urine panel / UACR on index date.

Patient IDs:
- Eligible: P0001–P0005
- Ineligible: P0006–P0010 (see manifest for reasons)
