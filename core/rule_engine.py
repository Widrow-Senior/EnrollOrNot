from typing import Any, Dict, List

def apply_operator(value: Any, op: str, threshold: Any) -> bool:
    """
    Применяет оператор к значению и порогу.
    Поддерживаемые операторы: '>=', '<=', '==', '>', '<', '!='
    """
    if op == ">=":
        return value >= threshold
    elif op == "<=":
        return value <= threshold
    elif op == ">":
        return value > threshold
    elif op == "<":
        return value < threshold
    elif op == "==":
        return value == threshold
    elif op == "!=":
        return value != threshold
    else:
        raise ValueError(f"Unsupported operator: {op}")

def evaluate_patient(
    patient_profile: Dict[str, Any],
    protocol_rules: List[Dict]
) -> Dict[str, Any]:
    """
    Оценивает соответствие пациента протоколу.

    Аргументы:
        patient_profile: словарь вида {"lvef": 35, "egfr": 45, ...}
        protocol_rules: список правил из YAML, каждый элемент:
            {
                "id": "R1",
                "type": "inclusion" или "exclusion",
                "field": "lvef",
                "operator": "<=",
                "value": 40
            }

    Возвращает:
        {
            "rule_results": [
                {"rule_id": "R1", "status": "passed" | "failed" | "missing"}
            ],
            "overall_status": "included" | "excluded" | "not enough information"
        }
    """
    rule_results = []
    has_missing = False

    for rule in protocol_rules:
        field = rule["field"]
        if field not in patient_profile or patient_profile[field] is None:
            rule_results.append({"rule_id": rule["id"], "status": "missing"})
            has_missing = True
            continue

        value = patient_profile[field]
        threshold = rule["value"]
        op = rule["operator"]

        try:
            passed = apply_operator(value, op, threshold)
        except Exception as e:
            # Если типы несовместимы (редко), считаем как нарушение
            rule_results.append({"rule_id": rule["id"], "status": "failed"})
            continue

        status = "passed" if passed else "failed"
        rule_results.append({"rule_id": rule["id"], "status": status})

    # Определяем итоговый статус
    if has_missing:
        overall_status = "not enough information"
    else:
        # Проверяем: если есть ЛЮБОЕ failed-правило типа "exclusion" → excluded
        # Или: если НЕ ВСЕ inclusion-правила passed → excluded
        exclusion_failed = any(
            r["status"] == "failed" for r in rule_results
            if next((rule for rule in protocol_rules if rule["id"] == r["rule_id"]), {}).get("type") == "exclusion"
        )
        inclusion_not_passed = any(
            r["status"] == "failed" for r in rule_results
            if next((rule for rule in protocol_rules if rule["id"] == r["rule_id"]), {}).get("type") == "inclusion"
        )

        if exclusion_failed or inclusion_not_passed:
            overall_status = "excluded"
        else:
            overall_status = "included"

    return {
        "rule_results": rule_results,
        "overall_status": overall_status
    }