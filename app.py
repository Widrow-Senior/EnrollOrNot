import streamlit as st
import pandas as pd
from core.rule_engine import evaluate_patient
from protocol_loader import load_protocol_yaml
from data_adapters.block1_adapter import adapt_block1
from data_adapters.block2_adapter import adapt_block2

# === Настройка страницы ===
st.set_page_config(
    page_title="EnrollOrNot",
    page_icon="🧠",
    layout="wide"
)

# === Заголовок ===
st.title("🧠 EnrollOrNot")
st.caption("Explainable, Traceable Eligibility Screening for Clinical Trials & RWE")

# === Данные Block 1 ===
def load_block1_data():
    """Загружает данные Block 1 с автоматическим определением кодировки"""
    try:
        return pd.read_csv("data/block1_data.tsv", sep="\t", encoding="cp1252")
    except:
        return pd.read_csv("data/block1_data.tsv", sep="\t", encoding="utf-8")

# === Выбор сценария ===
scenario = st.selectbox(
    "Select Scenario",
    [
        "Block 1: DAPA-HF",
        "Block 1: SIGIR-20141",
        "Block 2: Study W01",
        "Block 2: Study W02"
    ],
    key="scenario_selector"
)

# === Обработка Block 1 ===
if "Block 1" in scenario:
    df_block1 = load_block1_data()
    
    if "DAPA-HF" in scenario:
        protocol = load_protocol_yaml("protocols/dapa_hf.yaml")
        trial_id = "NCT03036124"
        filtered_df = df_block1[df_block1["trial_id"] == trial_id]
    else:  # SIGIR-20141
        protocol = load_protocol_yaml("protocols/sigir_20141.yaml")
        trial_id = "NCT03057977"  # ✅ ИСПРАВЛЕНО!
        filtered_df = df_block1[df_block1["trial_id"] == trial_id]
    
    if filtered_df.empty:
        st.error(f"No data found for trial {trial_id}")
        st.write("Available trial_ids in dataset:", df_block1["trial_id"].unique().tolist())
    else:
        patient_id = st.selectbox(
            "Select Patient",
            filtered_df["patient_id"].tolist(),
            key="block1_patient"
        )
        if patient_id:
            row = filtered_df[filtered_df["patient_id"] == patient_id].iloc[0].to_dict()
            profile = adapt_block1(row)
            result = evaluate_patient(profile.dict(), protocol)
            
            # Визуализация статуса
            status_color = {
                "included": "🟢",
                "excluded": "🔴",
                "not enough information": "⚠️"
            }
            status_display = result['overall_status'].replace("_", " ").title()
            st.subheader(f"{status_color.get(result['overall_status'], '❓')} **{status_display}**")
            st.write(f"**Initial Assessment**: {row.get('expert_eligibility', 'N/A')}")
            
            # Пояснение для неопределённого статуса
            if result['overall_status'] == "not enough information":
                st.info("💡 Decision requires additional data. See missing fields below.")
                rule_id_to_field = {r["id"]: r["field"] for r in protocol}
                missing_fields = []
                for r in result["rule_results"]:
                    if r["status"] == "missing":
                        field = rule_id_to_field.get(r["rule_id"], r["rule_id"])
                        missing_fields.append(field)
                if missing_fields:
                    st.write(f"**Missing data**: {', '.join(missing_fields)}")
            
            # Детали по правилам
            with st.expander("Rule-by-Rule Breakdown"):
                for rule_res in result["rule_results"]:
                    rule = next(r for r in protocol if r["id"] == rule_res["rule_id"])
                    status = rule_res["status"]
                    icon = "✅" if status == "passed" else "❌" if status == "failed" else "❓"
                    st.markdown(f"{icon} **{rule['description']}** → `{status.upper()}`")

# === Обработка Block 2: W01 ===
elif "W01" in scenario:
    eligible_ids = [f"P{str(i).zfill(4)}" for i in range(1, 6)]
    ineligible_ids = [f"P{str(i).zfill(4)}" for i in range(6, 11)]
    all_ids = eligible_ids + ineligible_ids
    
    patient_id = st.selectbox(
        "Select Patient",
        all_ids,
        key="w01_patient"
    )
    if patient_id:
        base_path = "data/Study W01/Eligible Patients" if patient_id in eligible_ids else "data/Study W01/Not Eligible Patients"
        profile = adapt_block2(patient_id, base_path)
        protocol = load_protocol_yaml("protocols/w01.yaml")
        result = evaluate_patient(profile.dict(), protocol)
        
        status_color = {
            "included": "🟢",
            "excluded": "🔴",
            "not enough information": "⚠️"
        }
        status_display = result['overall_status'].replace("_", " ").title()
        st.subheader(f"{status_color.get(result['overall_status'], '❓')} **{status_display}**")
        ground_truth = "eligible" if patient_id in eligible_ids else "ineligible"
        st.write(f"**Initial Assessment**: {ground_truth}")
        
        # Пояснение для неопределённого статуса
        if result['overall_status'] == "not enough information":
            st.info("💡 Decision requires additional data. See missing fields below.")
            rule_id_to_field = {r["id"]: r["field"] for r in protocol}
            missing_fields = []
            for r in result["rule_results"]:
                if r["status"] == "missing":
                    field = rule_id_to_field.get(r["rule_id"], r["rule_id"])
                    missing_fields.append(field)
            if missing_fields:
                st.write(f"**Missing data**: {', '.join(missing_fields)}")
        
        with st.expander("Rule-by-Rule Breakdown"):
            for rule_res in result["rule_results"]:
                rule = next(r for r in protocol if r["id"] == rule_res["rule_id"])
                status = rule_res["status"]
                icon = "✅" if status == "passed" else "❌" if status == "failed" else "❓"
                st.markdown(f"{icon} **{rule['description']}** → `{status.upper()}`")

# === Обработка Block 2: W02 ===
else:  # W02
    eligible_ids = [f"S{str(i).zfill(4)}" for i in range(1, 16)]
    ineligible_ids = [f"S{str(i).zfill(4)}" for i in range(16, 31)]
    all_ids = eligible_ids + ineligible_ids
    
    patient_id = st.selectbox(
        "Select Patient",
        all_ids,
        key="w02_patient"
    )
    if patient_id:
        base_path = "data/Study W02/Eligible Patients" if patient_id in eligible_ids else "data/Study W02/Not Eligible Patients"
        profile = adapt_block2(patient_id, base_path)
        protocol = load_protocol_yaml("protocols/w02.yaml")
        result = evaluate_patient(profile.dict(), protocol)
        
        status_color = {
            "included": "🟢",
            "excluded": "🔴",
            "not enough information": "⚠️"
        }
        status_display = result['overall_status'].replace("_", " ").title()
        st.subheader(f"{status_color.get(result['overall_status'], '❓')} **{status_display}**")
        ground_truth = "eligible" if patient_id in eligible_ids else "ineligible"
        st.write(f"**Initial Assessment**: {ground_truth}")
        
        # Пояснение для неопределённого статуса
        if result['overall_status'] == "not enough information":
            st.info("💡 Decision requires additional data. See missing fields below.")
            rule_id_to_field = {r["id"]: r["field"] for r in protocol}
            missing_fields = []
            for r in result["rule_results"]:
                if r["status"] == "missing":
                    field = rule_id_to_field.get(r["rule_id"], r["rule_id"])
                    missing_fields.append(field)
            if missing_fields:
                st.write(f"**Missing data**: {', '.join(missing_fields)}")
        
        with st.expander("Rule-by-Rule Breakdown"):
            for rule_res in result["rule_results"]:
                rule = next(r for r in protocol if r["id"] == rule_res["rule_id"])
                status = rule_res["status"]
                icon = "✅" if status == "passed" else "❌" if status == "failed" else "❓"
                st.markdown(f"{icon} **{rule['description']}** → `{status.upper()}`")