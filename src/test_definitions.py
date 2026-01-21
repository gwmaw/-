"""
검사 항목 정의 및 정상 범위 데이터
"""

# 검사 항목 그룹 정의
TEST_GROUPS = {
    "liver": {
        "name": "간기능 검사",
        "icon": "🫀",
        "color": "#FF6B6B",
        "tests": [
            "AST", "SGOT", "AST(SGOT)",
            "ALT", "SGPT", "ALT(SGPT)",
            "GGT", "γ-GTP", "Gamma-GT",
            "Total Bilirubin", "T-Bil", "Bilirubin",
            "ALP", "Alkaline Phosphatase"
        ]
    },
    "kidney": {
        "name": "신기능 검사",
        "icon": "🫘",
        "color": "#4ECDC4",
        "tests": [
            "BUN", "Blood Urea Nitrogen",
            "Creatinine", "Cr",
            "eGFR", "GFR",
            "Uric Acid", "UA"
        ]
    },
    "diabetes": {
        "name": "당뇨 검사",
        "icon": "🍬",
        "color": "#FFE66D",
        "tests": [
            "Glucose", "FBS", "Fasting Glucose", "공복혈당",
            "HbA1c", "Hemoglobin A1c", "당화혈색소"
        ]
    },
    "lipid": {
        "name": "지질 검사",
        "icon": "🧈",
        "color": "#FF8C42",
        "tests": [
            "Total Cholesterol", "T-Chol", "Cholesterol", "총콜레스테롤",
            "LDL", "LDL-C", "LDL Cholesterol",
            "HDL", "HDL-C", "HDL Cholesterol",
            "Triglyceride", "TG", "중성지방"
        ]
    },
    "blood": {
        "name": "혈액학 검사",
        "icon": "🩸",
        "color": "#C44569",
        "tests": [
            "WBC", "White Blood Cell", "백혈구",
            "RBC", "Red Blood Cell", "적혈구",
            "Hemoglobin", "Hgb", "Hb", "혈색소",
            "Hematocrit", "Hct", "헤마토크릿",
            "Platelet", "PLT", "혈소판"
        ]
    },
    "thyroid": {
        "name": "갑상선 검사",
        "icon": "🦋",
        "color": "#A8E6CF",
        "tests": [
            "TSH", "Thyroid Stimulating Hormone",
            "Free T4", "FT4", "Free Thyroxine",
            "Free T3", "FT3"
        ]
    },
    "urine": {
        "name": "소변 검사",
        "icon": "💧",
        "color": "#95E1D3",
        "tests": [
            "Urine Protein", "U-Protein", "단백뇨",
            "Urine Glucose", "U-Glucose", "당뇨",
            "Urine Blood", "U-Blood", "잠혈",
            "pH", "Urine pH"
        ]
    }
}

# 검사 항목별 정상 범위 (성별, 나이 고려 가능)
REFERENCE_RANGES = {
    # 간기능
    "AST": {"min": 0, "max": 40, "unit": "U/L"},
    "SGOT": {"min": 0, "max": 40, "unit": "U/L"},
    "AST(SGOT)": {"min": 0, "max": 40, "unit": "U/L"},
    "ALT": {"min": 0, "max": 40, "unit": "U/L"},
    "SGPT": {"min": 0, "max": 40, "unit": "U/L"},
    "ALT(SGPT)": {"min": 0, "max": 40, "unit": "U/L"},
    "GGT": {"min": 0, "max": 60, "unit": "U/L"},
    "γ-GTP": {"min": 0, "max": 60, "unit": "U/L"},
    "Gamma-GT": {"min": 0, "max": 60, "unit": "U/L"},
    "Total Bilirubin": {"min": 0.2, "max": 1.2, "unit": "mg/dL"},
    "T-Bil": {"min": 0.2, "max": 1.2, "unit": "mg/dL"},
    "Bilirubin": {"min": 0.2, "max": 1.2, "unit": "mg/dL"},
    "ALP": {"min": 30, "max": 120, "unit": "U/L"},
    "Alkaline Phosphatase": {"min": 30, "max": 120, "unit": "U/L"},
    
    # 신기능
    "BUN": {"min": 8, "max": 20, "unit": "mg/dL"},
    "Blood Urea Nitrogen": {"min": 8, "max": 20, "unit": "mg/dL"},
    "Creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
    "Cr": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
    "eGFR": {"min": 90, "max": 999, "unit": "mL/min/1.73m²"},
    "GFR": {"min": 90, "max": 999, "unit": "mL/min/1.73m²"},
    "Uric Acid": {"min": 3.5, "max": 7.0, "unit": "mg/dL"},
    "UA": {"min": 3.5, "max": 7.0, "unit": "mg/dL"},
    
    # 당뇨
    "Glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
    "FBS": {"min": 70, "max": 100, "unit": "mg/dL"},
    "Fasting Glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
    "공복혈당": {"min": 70, "max": 100, "unit": "mg/dL"},
    "HbA1c": {"min": 4.0, "max": 5.6, "unit": "%"},
    "Hemoglobin A1c": {"min": 4.0, "max": 5.6, "unit": "%"},
    "당화혈색소": {"min": 4.0, "max": 5.6, "unit": "%"},
    
    # 지질
    "Total Cholesterol": {"min": 0, "max": 200, "unit": "mg/dL"},
    "T-Chol": {"min": 0, "max": 200, "unit": "mg/dL"},
    "Cholesterol": {"min": 0, "max": 200, "unit": "mg/dL"},
    "총콜레스테롤": {"min": 0, "max": 200, "unit": "mg/dL"},
    "LDL": {"min": 0, "max": 130, "unit": "mg/dL"},
    "LDL-C": {"min": 0, "max": 130, "unit": "mg/dL"},
    "LDL Cholesterol": {"min": 0, "max": 130, "unit": "mg/dL"},
    "HDL": {"min": 40, "max": 999, "unit": "mg/dL"},
    "HDL-C": {"min": 40, "max": 999, "unit": "mg/dL"},
    "HDL Cholesterol": {"min": 40, "max": 999, "unit": "mg/dL"},
    "Triglyceride": {"min": 0, "max": 150, "unit": "mg/dL"},
    "TG": {"min": 0, "max": 150, "unit": "mg/dL"},
    "중성지방": {"min": 0, "max": 150, "unit": "mg/dL"},
    
    # 혈액학
    "WBC": {"min": 4.0, "max": 10.0, "unit": "10³/μL"},
    "White Blood Cell": {"min": 4.0, "max": 10.0, "unit": "10³/μL"},
    "백혈구": {"min": 4.0, "max": 10.0, "unit": "10³/μL"},
    "RBC": {"min": 4.2, "max": 6.0, "unit": "10⁶/μL"},
    "Red Blood Cell": {"min": 4.2, "max": 6.0, "unit": "10⁶/μL"},
    "적혈구": {"min": 4.2, "max": 6.0, "unit": "10⁶/μL"},
    "Hemoglobin": {"min": 12.0, "max": 18.0, "unit": "g/dL"},
    "Hgb": {"min": 12.0, "max": 18.0, "unit": "g/dL"},
    "Hb": {"min": 12.0, "max": 18.0, "unit": "g/dL"},
    "혈색소": {"min": 12.0, "max": 18.0, "unit": "g/dL"},
    "Hematocrit": {"min": 37.0, "max": 52.0, "unit": "%"},
    "Hct": {"min": 37.0, "max": 52.0, "unit": "%"},
    "헤마토크릿": {"min": 37.0, "max": 52.0, "unit": "%"},
    "Platelet": {"min": 150, "max": 400, "unit": "10³/μL"},
    "PLT": {"min": 150, "max": 400, "unit": "10³/μL"},
    "혈소판": {"min": 150, "max": 400, "unit": "10³/μL"},
    
    # 갑상선
    "TSH": {"min": 0.4, "max": 4.0, "unit": "μIU/mL"},
    "Thyroid Stimulating Hormone": {"min": 0.4, "max": 4.0, "unit": "μIU/mL"},
    "Free T4": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
    "FT4": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
    "Free Thyroxine": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
    "Free T3": {"min": 2.3, "max": 4.2, "unit": "pg/mL"},
    "FT3": {"min": 2.3, "max": 4.2, "unit": "pg/mL"},
    
    # 소변
    "Urine Protein": {"value": "Negative", "unit": ""},
    "U-Protein": {"value": "Negative", "unit": ""},
    "단백뇨": {"value": "Negative", "unit": ""},
    "Urine Glucose": {"value": "Negative", "unit": ""},
    "U-Glucose": {"value": "Negative", "unit": ""},
    "당뇨": {"value": "Negative", "unit": ""},
    "Urine Blood": {"value": "Negative", "unit": ""},
    "U-Blood": {"value": "Negative", "unit": ""},
    "잠혈": {"value": "Negative", "unit": ""},
    "pH": {"min": 5.0, "max": 8.0, "unit": ""},
    "Urine pH": {"min": 5.0, "max": 8.0, "unit": ""},
}


def find_test_group(test_name):
    """검사 항목명으로 그룹 찾기"""
    for group_key, group_info in TEST_GROUPS.items():
        for test in group_info["tests"]:
            if test.lower() in test_name.lower() or test_name.lower() in test.lower():
                return group_key
    return None


def get_reference_range(test_name):
    """검사 항목명으로 정상 범위 가져오기"""
    # 정확한 매칭 시도
    if test_name in REFERENCE_RANGES:
        return REFERENCE_RANGES[test_name]
    
    # 부분 매칭 시도
    for ref_name, ref_range in REFERENCE_RANGES.items():
        if ref_name.lower() in test_name.lower() or test_name.lower() in ref_name.lower():
            return ref_range
    
    return None


def is_abnormal(test_name, value):
    """검사 결과가 이상인지 판별"""
    ref_range = get_reference_range(test_name)
    if not ref_range:
        return False
    
    try:
        # 수치형 비교
        if "min" in ref_range and "max" in ref_range:
            value_num = float(value)
            return value_num < ref_range["min"] or value_num > ref_range["max"]
        
        # 문자형 비교 (Negative 등)
        if "value" in ref_range:
            return str(value).strip().lower() != str(ref_range["value"]).lower()
    except (ValueError, TypeError):
        return False
    
    return False


def get_abnormal_direction(test_name, value):
    """이상 방향 (높음/낮음) 판별"""
    ref_range = get_reference_range(test_name)
    if not ref_range or "min" not in ref_range:
        return None
    
    try:
        value_num = float(value)
        if value_num < ref_range["min"]:
            return "low"
        elif value_num > ref_range["max"]:
            return "high"
    except (ValueError, TypeError):
        pass
    
    return None
