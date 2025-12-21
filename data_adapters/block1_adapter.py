import re
from typing import Dict, Any
from core.models import PatientProfile

def extract_lvef(note: str) -> float:
    match = re.search(r'(?:LVEF|ejection fraction)[^0-9]*?(\d+\.?\d*)%', note, re.IGNORECASE)
    return float(match.group(1)) if match else None

def extract_nt_probnp(note: str) -> float:
    match = re.search(r'NT-proBNP\D*(\d[\d,]*)', note, re.IGNORECASE)
    return float(match.group(1).replace(',', '')) if match else None

def extract_egfr(note: str) -> float:
    match = re.search(r'eGFR\D*(\d+\.?\d*)', note, re.IGNORECASE)
    return float(match.group(1)) if match else None

def extract_systolic_bp(note: str) -> int:
    match = re.search(r'(\d+)/\d+\s*mmHg', note, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_diastolic_bp(note: str) -> int:
    match = re.search(r'\d+/(\d+)\s*mmHg', note, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_sglt2_inhibitor(note: str) -> bool:
    note_lower = note.lower()
    sglt2_found = any(drug in note_lower for drug in ['empagliflozin', 'dapagliflozin', 'canagliflozin'])
    if sglt2_found:
        return not any(neg in note_lower for neg in ['no history', 'never received', 'not received'])
    return False

def extract_type1_diabetes(note: str) -> bool:
    note_lower = note.lower()
    return 'type 1 diabetes' in note_lower and 'no history' not in note_lower

def extract_nyha_class(note: str) -> int:
    match = re.search(r'NYHA class (II|III|IV|II–III|II-III)', note, re.IGNORECASE)
    if match:
        nyha_str = match.group(1)
        if 'II' in nyha_str and ('III' in nyha_str or 'IV' in nyha_str):
            return 3
        return {'II': 2, 'III': 3, 'IV': 4}.get(nyha_str.strip(), None)
    return None

def extract_gdmtd_therapy(note: str) -> bool:
    note_lower = note.lower()
    has_ace_arni = 'ace inhibitor' in note_lower or 'arni' in note_lower
    has_beta = 'beta-blocker' in note_lower
    has_mra = 'mra' in note_lower or 'mineralocorticoid receptor antagonist' in note_lower
    has_diuretic = 'diuretic' in note_lower
    return sum([has_ace_arni, has_beta, has_mra, has_diuretic]) >= 2

def extract_age(note: str) -> int:
    match = re.search(r'(\d+)-year-old', note, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_gender(note: str) -> str:
    match = re.search(r'(woman|man|female|male)', note, re.IGNORECASE)
    if match:
        gender = match.group(1).lower()
        return 'female' if gender in ('woman', 'female') else 'male'
    return None

# --- SIGIR-20141 specific fields ---
def extract_congestive_hf(note: str) -> bool:
    n = note.lower()
    return 'congestive' in n or 'heart failure' in n or 'hf' in n

def extract_unstable_angina(note: str) -> bool:
    n = note.lower()
    unstable_phrases = [
        'unstable angina', 'at rest', 'worsening', 'new-onset',
        'first time in life', 'acute coronary syndrome'
    ]
    return any(phrase in n for phrase in unstable_phrases)

def extract_calcium_channel_blocker(note: str) -> bool:
    n = note.lower()
    return 'calcium channel blocker' in n or 'ccb' in n or 'amlodipine' in n

def extract_sbp(note: str) -> int:
    # sbp = systolic blood pressure (дублирует bp_systolic для удобства)
    return extract_systolic_bp(note)

def adapt_block1(row: Dict[str, Any]) -> PatientProfile:
    note = row["note"]
    return PatientProfile(
        patient_id=row["patient_id"],
        age=extract_age(note),
        gender=extract_gender(note),
        lvef=extract_lvef(note),
        nt_probnp=extract_nt_probnp(note),
        egfr=extract_egfr(note),
        nyha_class=extract_nyha_class(note),
        gdmtd_hf_therapy=extract_gdmtd_therapy(note),
        sglt2_inhibitor=extract_sglt2_inhibitor(note),
        type1_diabetes=extract_type1_diabetes(note),
        bp_systolic=extract_systolic_bp(note),
        bp_diastolic=extract_diastolic_bp(note),
        # --- SIGIR fields ---
        congestive_hf=extract_congestive_hf(note),
        unstable_angina=extract_unstable_angina(note),
        calcium_channel_blocker=extract_calcium_channel_blocker(note),
        sbp=extract_sbp(note),
        source_files={"note": "clinical_note"}
    )