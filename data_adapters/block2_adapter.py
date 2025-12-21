import pandas as pd
import os
from core.models import PatientProfile

def adapt_block2(patient_id: str, base_path: str) -> PatientProfile:
    profile = {
        "patient_id": patient_id,
        "type1_diabetes": False,  # Устанавливаем по умолчанию СРАЗУ
        "source_files": {}
    }
    
    # === 1. Текст от врача ===
    note = None
    note_source = None

    # Study W02
    clinical_note_path = os.path.join(base_path, f"{patient_id}_clinical_note.csv")
    if os.path.exists(clinical_note_path):
        df = pd.read_csv(clinical_note_path)
        if not df.empty and "narrative_note" in df.columns:
            raw_note = df["narrative_note"].iloc[0]
            if pd.notna(raw_note) and str(raw_note).strip():
                note = str(raw_note).strip()
                note_source = clinical_note_path

    # Study W01
    if note is None:
        anamnesis_path = os.path.join(base_path, f"{patient_id}_anamnesis.csv")
        if os.path.exists(anamnesis_path):
            df = pd.read_csv(anamnesis_path)
            if not df.empty and "narrative_note" in df.columns:
                raw_note = df["narrative_note"].iloc[0]
                if pd.notna(raw_note) and str(raw_note).strip():
                    note = str(raw_note).strip()
                    note_source = anamnesis_path

    # Анализ текста (только если есть непустой текст)
    if note:
        note_lower = note.lower()
        has_type1 = "type 1 diabetes" in note_lower
        has_negation = (
            "no history" in note_lower or
            "not type 1" in note_lower or
            "type 2 diabetes" in note_lower or
            "type II diabetes" in note_lower
        )
        profile["type1_diabetes"] = has_type1 and not has_negation
        profile["source_files"]["clinical_note"] = note_source
    # Если текста нет — остаётся False (уже задано выше)

    # === 2. Лабораторные анализы ===
    labs_df = None
    labs_source = None

    renal_labs_path = os.path.join(base_path, f"{patient_id}_renal_labs.csv")
    if os.path.exists(renal_labs_path):
        labs_df = pd.read_csv(renal_labs_path)
        labs_source = renal_labs_path

    if labs_df is None:
        blood_labs_path = os.path.join(base_path, f"{patient_id}_blood_labs.csv")
        if os.path.exists(blood_labs_path):
            labs_df = pd.read_csv(blood_labs_path)
            labs_source = blood_labs_path

    if labs_df is not None and not labs_df.empty:
        if "test_name" in labs_df.columns and "value" in labs_df.columns:
            for _, row in labs_df[::-1].iterrows():
                test_name = str(row["test_name"])
                value = row["value"]
                if profile.get("egfr") is None and ("eGFR" in test_name or "egfr" in test_name.lower()):
                    try:
                        profile["egfr"] = float(value)
                    except (ValueError, TypeError):
                        pass
                if profile.get("hba1c") is None and ("HbA1c" in test_name or "hba1c" in test_name.lower()):
                    try:
                        profile["hba1c"] = float(value)
                    except (ValueError, TypeError):
                        pass
        elif "egfr" in labs_df.columns:
            last_valid = labs_df["egfr"].dropna()
            if not last_valid.empty:
                profile["egfr"] = float(last_valid.iloc[-1])
        if labs_source:
            profile["source_files"]["labs"] = labs_source

    # === 3. UACR (только W01) ===
    urinalysis_path = os.path.join(base_path, f"{patient_id}_urinalysis.csv")
    if os.path.exists(urinalysis_path):
        df = pd.read_csv(urinalysis_path)
        if not df.empty and "test_name" in df.columns and "value" in df.columns:
            for _, row in df[::-1].iterrows():
                test_name = str(row["test_name"])
                value = row["value"]
                if profile.get("uacr") is None:
                    test_lower = test_name.lower()
                    if ("albumin" in test_lower and "creatinine" in test_lower) or "uacr" in test_lower:
                        try:
                            profile["uacr"] = float(value)
                        except (ValueError, TypeError):
                            pass
            profile["source_files"]["urinalysis"] = urinalysis_path

    return PatientProfile(**profile)