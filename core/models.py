from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Rule(BaseModel):
    id: str
    type: str = Field(..., pattern="^(inclusion|exclusion)$")
    field: str
    operator: str = Field(..., pattern="^(>=|<=|==|>|<|!=)$")
    value: Any
    description: Optional[str] = None

class PatientProfile(BaseModel):
    patient_id: str

    # --- Общие ---
    age: Optional[int] = None
    gender: Optional[str] = None

    # --- DAPA-HF ---
    lvef: Optional[float] = None
    nt_probnp: Optional[float] = None
    nyha_class: Optional[int] = None
    gdmtd_hf_therapy: Optional[bool] = None
    egfr: Optional[float] = None
    sglt2_inhibitor: Optional[bool] = None
    type1_diabetes: Optional[bool] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None

    # --- SIGIR-20141 (добавлено) ---
    congestive_hf: Optional[bool] = None
    unstable_angina: Optional[bool] = None
    calcium_channel_blocker: Optional[bool] = None
    sbp: Optional[int] = None  # systolic blood pressure (альтернатива bp_systolic)

    # --- W01/W02 ---
    hba1c: Optional[float] = None
    uacr: Optional[float] = None

    # --- Трассировка ---
    source_files: Optional[Dict[str, str]] = None

class RuleResult(BaseModel):
    rule_id: str
    status: str = Field(..., pattern="^(passed|failed|missing)$")

class EvaluationResult(BaseModel):
    patient_id: str
    rule_results: List[RuleResult]
    overall_status: str = Field(..., pattern="^(included|excluded|not enough information)$")

    def get_rule_status(self, rule_id: str) -> str:
        for r in self.rule_results:
            if r.rule_id == rule_id:
                return r.status
        return "unknown"