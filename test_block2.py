import os
from data_adapters.block2_adapter import adapt_block2

def test_study_w01():
    print("=== Тестирование Study W01 ===")
    
    # Eligible: P0001–P0005
    eligible_ids = [f"P{str(i).zfill(4)}" for i in range(1, 6)]
    # Ineligible: P0006–P0010
    ineligible_ids = [f"P{str(i).zfill(4)}" for i in range(6, 11)]
    
    base_eligible = "data/Study W01/Eligible Patients"
    base_ineligible = "data/Study W01/Not Eligible Patients"
    
    for pid in eligible_ids[:2]:
        try:
            profile = adapt_block2(pid, base_eligible)
            print(f" {pid} (eligible): egfr={profile.egfr}, uacr={profile.uacr}, type1_dm={profile.type1_diabetes}")
        except Exception as e:
            print(f" {pid} (eligible): ошибка — {e}")
    
    for pid in ineligible_ids[:2]:
        try:
            profile = adapt_block2(pid, base_ineligible)
            print(f" {pid} (ineligible): egfr={profile.egfr}, uacr={profile.uacr}, type1_dm={profile.type1_diabetes}")
        except Exception as e:
            print(f" {pid} (ineligible): ошибка — {e}")

def test_study_w02():
    print("\n=== Тестирование Study W02 ===")
    
    # Eligible: S0001–S0015
    eligible_ids = [f"S{str(i).zfill(4)}" for i in range(1, 16)]
    # Ineligible: S0016–S0030
    ineligible_ids = [f"S{str(i).zfill(4)}" for i in range(16, 31)]
    
    base_eligible = "data/Study W02/Eligible Patients"
    base_ineligible = "data/Study W02/Not Eligible Patients"
    
    for pid in eligible_ids[:2]:
        try:
            profile = adapt_block2(pid, base_eligible)
            print(f" {pid} (eligible): egfr={profile.egfr}, uacr={profile.uacr}, type1_dm={profile.type1_diabetes}")
        except Exception as e:
            print(f" {pid} (eligible): ошибка — {e}")
    
    for pid in ineligible_ids[:2]:
        try:
            profile = adapt_block2(pid, base_ineligible)
            print(f" {pid} (ineligible): egfr={profile.egfr}, uacr={profile.uacr}, type1_dm={profile.type1_diabetes}")
        except Exception as e:
            print(f" {pid} (ineligible): ошибка — {e}")

if __name__ == "__main__":
    # Проверка существования всех папок
    required_paths = [
        "data/Study W01/Eligible Patients",
        "data/Study W01/Not Eligible Patients",
        "data/Study W02/Eligible Patients",
        "data/Study W02/Not Eligible Patients"
    ]
    
    for path in required_paths:
        if not os.path.exists(path):
            print(f" Критическая ошибка: папка не найдена — {path}")
            exit(1)
    
    test_study_w01()
    test_study_w02()
    print("\n Тест Block 2 завершён успешно")