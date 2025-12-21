import pandas as pd
from data_adapters.block1_adapter import adapt_block1

# Попытка загрузить с разными кодировками
encodings = ["utf-8", "cp1252", "windows-1251"]
df = None
used_encoding = None

for enc in encodings:
    try:
        df = pd.read_csv("data/block1_data.tsv", sep="\t", encoding=enc)
        used_encoding = enc
        break
    except UnicodeDecodeError:
        continue

if df is None:
    print("Не удалось загрузить файл ни с одной из кодировок:", encodings)
    exit()

print(f" TSV загружен (кодировка: {used_encoding}). Всего пациентов:", len(df))

# Дальше — тот же код...
first_row = df.iloc[0].to_dict()

print("\n=== Первый пациент ===")
print("patient_id:", first_row.get("patient_id"))
print("trial_id:", first_row.get("trial_id"))
print("expert_eligibility:", first_row.get("expert_eligibility"))

try:
    profile = adapt_block1(first_row)
    print("\n=== Извлечённый профиль ===")
    print("patient_id:", profile.patient_id)
    print("lvef:", profile.lvef)
    print("nt_probnp:", profile.nt_probnp)
    print("egfr:", profile.egfr)
    print("sglt2_inhibitor:", profile.sglt2_inhibitor)
    print("type1_diabetes:", profile.type1_diabetes)
    print("bp_systolic:", profile.bp_systolic)
    print("bp_diastolic:", profile.bp_diastolic)
except Exception as e:
    print(" Ошибка в адаптере:", e)
    raise