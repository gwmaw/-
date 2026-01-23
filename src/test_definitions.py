"""
검사 항목 정의 및 정상 범위 데이터
"""

# 검사 항목 그룹 정의
TEST_GROUPS = {
    "liver": {
        "name": "간기능 검사",
        "icon": "[간]",
        "color": "#FF6B6B",
        "tests": [
            "AST", "SGOT", "AST(SGOT)", "AST (SGPT)", "간기능(AST)",
            "ALT", "SGPT", "ALT(SGPT)", "ALT (SGPT)", "간기능(ALT)",
            "GGT", "γ-GTP", "Gamma-GT", "간기능(γ-GTP)", "γ-GT",
            "Total Bilirubin", "T-Bil", "Bilirubin", "황달수치", "총빌리루빈", "황달수치(T-bil)",
            "Direct Bilirubin", "D-Bil", "직접빌리루빈",
            "ALP", "Alkaline Phosphatase", "간기능(ALP)", "알칼리포스파타제",
            "총단백", "알부민"
        ]
    },
    "kidney": {
        "name": "신기능 검사",
        "icon": "[신]",
        "color": "#4ECDC4",
        "tests": [
            "BUN", "Blood Urea Nitrogen", "신장기능(BUN)",
            "Creatinine", "Cr", "신장기능(Cr)",
            "eGFR", "GFR", "사구체여과율", "사구체 여과율"
        ]
    },
    "diabetes": {
        "name": "당뇨 검사",
        "icon": "[당]",
        "color": "#FFE66D",
        "tests": [
            "Glucose", "FBS", "Fasting Glucose", "공복혈당", "당검사",
            "HbA1c", "Hemoglobin A1c", "당화혈색소",
            "HbA1c-NGSP"
        ]
    },
    "lipid": {
        "name": "지질 검사",
        "icon": "[지]",
        "color": "#FF8C42",
        "tests": [
            "Total Cholesterol", "T-Chol", "Cholesterol", "총콜레스테롤",
            "LDL", "LDL-C", "LDL Cholesterol", "저밀도콜레스테롤",
            "HDL", "HDL-C", "HDL Cholesterol", "고밀도콜레스테롤",
            "Triglyceride", "TG", "중성지방"
        ]
    },
    "blood": {
        "name": "혈액학 검사",
        "icon": "[혈]",
        "color": "#C44569",
        "tests": [
            "WBC", "White Blood Cell", "백혈구", "백혈구수",
            "RBC", "Red Blood Cell", "적혈구", "적혈구수",
            "Hemoglobin", "Hgb", "Hb", "혈색소", "HB", "헤모글로빈", "빈혈수치",
            "Hematocrit", "Hct", "헤마토크릿", "헤마토크리트",
            "Platelet", "PLT", "혈소판", "혈소판수",
            "MCV", "MCH", "MCHC",
            "Diff Count", "Diff",
            "Seg.Neutrophil", "Segment neutrophil", "Segment Neutrophil",
            "Lymphocyte", "Monocyte", "Eosinophil", "Basophil"
        ]
    },
    "thyroid": {
        "name": "갑상선 검사",
        "icon": "[갑]",
        "color": "#A8E6CF",
        "tests": [
            "TSH", "Thyroid Stimulating Hormone", "갑상선자극호르몬",
            "Free T4", "FT4", "Free Thyroxine", "갑상선호르몬[Free T4]",
            "Free T3", "FT3", "갑상선호르몬[T3]", "T3"
        ]
    },
    "electrolyte": {
        "name": "전해질 검사",
        "icon": "[전]",
        "color": "#FFB6C1",
        "tests": [
            "나트륨", "Sodium", "Na",
            "염소", "Chloride", "Cl",
            "칼륨", "Potassium", "K",
            "칼슘", "Calcium", "Ca",
            "마그네슘", "Magnesium", "Mg"
        ]
    },
    "urine": {
        "name": "소변 검사",
        "icon": "[소]",
        "color": "#95E1D3",
        "tests": [
            # 소변검사-10종
            "소변검사-10종", "소변검사", "요검사",
            "color", "색", "색조",
            "turbidity", "혼탁도", "탁도",
            "Blood", "잠혈", "요잠혈", "Urine Blood", "U-Blood", "Occult Blood",
            "Bilirubin", "빌리루빈", "요빌리루빈",
            "Urobilinogen", "유로빌리노겐",
            "Ketone", "케톤", "케톤체",
            "Protein", "단백", "요단백", "Urine Protein", "U-Protein", "단백뇨",
            "Nitrite", "아질산염", "질산염",
            "Glucose", "당", "요당", "Urine Glucose", "U-Glucose",
            "pH", "Urine pH", "수소이온농도",
            "Specific Gravity", "S.G", "비중",
            "Leukocyte", "Leukocyte esterase", "백혈구",
            # 요침사검사-현미경관찰
            "요침사검사-현미경관찰", "요침사검사", "현미경관찰",
            "Micro RBC", "Micro Red Blood Cell",
            "Micro WBC", "Micro White Blood Cell",
            "Micro Epithelial cell", "상피세포",
            "Micro Bacteria", "세균",
            "Micro Yeast like cell", "효모양세포",
            # 기타 소변 관련
            "크레아티닌-정밀검사(urine)", "크레아티닌",
            "요 알부민/크레아티닌비(ACR)", "알부민/크레아티닌비",
            "요단백"
        ]
    },
    "other": {
        "name": "기타 검사",
        "icon": "[기]",
        "color": "#9B59B6",
        "tests": [
            # 염증/면역 검사
            "CRP", "C-Reactive Protein", "C-반응성 단백", "염증수치", "염증수치(CRP)",
            # 통풍/요산 검사
            "Uric Acid", "UA", "요산", "통풍수치", "통풍수치-요산",
            # 기타
            "ESR", "적혈구침강속도"
        ]
    }
}

# 검사 항목별 정상 범위 (성별, 나이 고려 가능)
REFERENCE_RANGES = {
    # 간기능
    "AST": {"min": 0, "max": 40, "unit": "U/L"},
    "SGOT": {"min": 0, "max": 40, "unit": "U/L"},
    "AST(SGOT)": {"min": 0, "max": 40, "unit": "U/L"},
    "AST (SGOT)": {"min": 0, "max": 40, "unit": "IU/L"},
    "간기능(AST)": {"min": 0, "max": 40, "unit": "U/L"},
    "ALT": {"min": 0, "max": 41, "unit": "U/L"},
    "SGPT": {"min": 0, "max": 41, "unit": "U/L"},
    "ALT(SGPT)": {"min": 0, "max": 41, "unit": "U/L"},
    "ALT (SGPT)": {"min": 0, "max": 41, "unit": "IU/L"},
    "간기능(ALT)": {"min": 0, "max": 41, "unit": "U/L"},
    "GGT": {"min": 6, "max": 42, "unit": "U/L"},
    "γ-GTP": {"min": 11, "max": 61, "unit": "U/L"},
    "간기능(γ-GTP)": {"min": 11, "max": 61, "unit": "U/L"},
    "Gamma-GT": {"min": 6, "max": 42, "unit": "U/L"},
    "Total Bilirubin": {"min": 0.3, "max": 1.2, "unit": "mg/dL"},
    "T-Bil": {"min": 0.3, "max": 1.2, "unit": "mg/dL"},
    "총빌리루빈": {"min": 0.3, "max": 1.2, "unit": "mg/dL"},
    "황달수치(T-bil)": {"min": 0.3, "max": 1.2, "unit": "mg/dl"},
    "Bilirubin": {"min": 0.3, "max": 1.2, "unit": "mg/dL"},
    "Direct Bilirubin": {"min": 0.0, "max": 0.30, "unit": "mg/dL"},
    "D-Bil": {"min": 0.0, "max": 0.30, "unit": "mg/dL"},
    "직접빌리루빈": {"min": 0.0, "max": 0.30, "unit": "mg/dL"},
    "ALP": {"min": 35, "max": 240, "unit": "U/L"},
    "간기능(ALP)": {"min": 0, "max": 240, "unit": "U/L"},
    "알칼리포스파타제(ALP)": {"min": 35, "max": 104, "unit": "IU/L"},
    "Alkaline Phosphatase": {"min": 35, "max": 240, "unit": "U/L"},
    "총단백": {"min": 6.4, "max": 8.3, "unit": "g/dl"},
    "알부민": {"min": 3.5, "max": 5.2, "unit": "g/dl"},
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
    "요산": {"min": 3.5, "max": 7.0, "unit": "mg/dL"},
    "통풍수치": {"min": 3.4, "max": 7.0, "unit": "mg/dL"},
    "통풍수치-요산": {"min": 3.4, "max": 7.0, "unit": "mg/dL"},
    "통풍수치-요산(uric acid)": {"min": 3.4, "max": 7.0, "unit": "mg/dL"},
    "CRP": {"min": 0.0, "max": 0.5, "unit": "mg/dL"},
    "C-Reactive Protein": {"min": 0.0, "max": 0.5, "unit": "mg/dL"},
    "염증수치": {"min": 0.0, "max": 0.5, "unit": "mg/dL"},
    "염증수치(CRP)": {"min": 0.0, "max": 0.5, "unit": "mg/dL"},
    "C-반응성 단백": {"min": 0.0, "max": 0.5, "unit": "mg/dL"},
    
    # 당뇨
    "Glucose": {"min": 70, "max": 99, "unit": "mg/dL"},
    "FBS": {"min": 70, "max": 99, "unit": "mg/dL"},
    "Fasting Glucose": {"min": 70, "max": 99, "unit": "mg/dL"},
    "공복혈당": {"min": 70, "max": 99, "unit": "mg/dL"},
    "당검사[화학반응-장비측정][정량]": {"min": 70, "max": 99, "unit": "mg/dL"},
    "HbA1c": {"min": 4.5, "max": 5.6, "unit": "%"},
    "Hemoglobin A1c": {"min": 4.5, "max": 5.6, "unit": "%"},
    "당화혈색소": {"min": 4.5, "max": 5.6, "unit": "%"},
    "당화혈색소(HbA1c)": {"min": 4.5, "max": 5.6, "unit": "%"},
    "HbA1c-NGSP": {"min": 4.5, "max": 5.6, "unit": "%"},
    "HbA1c-IFCC": {"min": 20, "max": 42, "unit": "mmol/mol"},
    "HbA1c-eAG": {"min": 70, "max": 120, "unit": "mg/dL"},
    
    # 지질
    "Total Cholesterol": {"min": 0, "max": 199, "unit": "mg/dL"},
    "T-Chol": {"min": 0, "max": 199, "unit": "mg/dL"},
    "Cholesterol": {"min": 0, "max": 199, "unit": "mg/dL"},
    "총콜레스테롤": {"min": 0, "max": 199, "unit": "mg/dl"},
    "LDL": {"min": 0, "max": 130, "unit": "mg/dL"},
    "LDL-C": {"min": 0, "max": 130, "unit": "mg/dL"},
    "LDL Cholesterol": {"min": 0, "max": 130, "unit": "mg/dL"},
    "저밀도콜레스테롤": {"min": 0, "max": 130, "unit": "mg/dL"},
    "HDL": {"min": 60, "max": 999, "unit": "mg/dL"},
    "HDL-C": {"min": 60, "max": 999, "unit": "mg/dL"},
    "HDL Cholesterol": {"min": 60, "max": 999, "unit": "mg/dL"},
    "고밀도콜레스테롤(HDL)": {"min": 60, "max": 999, "unit": "mg/dl"},
    "Triglyceride": {"min": 0, "max": 149, "unit": "mg/dL"},
    "TG": {"min": 0, "max": 149, "unit": "mg/dL"},
    "TG(중성지방)": {"min": 0, "max": 149, "unit": "mg/dL"},
    "중성지방(TG)": {"min": 0, "max": 149, "unit": "mg/dl"},
    "중성지방": {"min": 0, "max": 149, "unit": "mg/dL"},
    "저밀도콜레스테롤(LDL)": {"min": 0, "max": 129, "unit": "mg/dL"},
    
    # 전해질
    "나트륨": {"min": 136, "max": 145, "unit": "mmol/L"},
    "Sodium": {"min": 136, "max": 145, "unit": "mmol/L"},
    "Na": {"min": 136, "max": 145, "unit": "mmol/L"},
    "염소": {"min": 98, "max": 107, "unit": "mmol/L"},
    "Chloride": {"min": 98, "max": 107, "unit": "mmol/L"},
    "Cl": {"min": 98, "max": 107, "unit": "mmol/L"},
    "칼륨": {"min": 3.5, "max": 5.1, "unit": "mmol/L"},
    "Potassium": {"min": 3.5, "max": 5.1, "unit": "mmol/L"},
    "K": {"min": 3.5, "max": 5.1, "unit": "mmol/L"},
    "칼슘": {"min": 8.5, "max": 10.5, "unit": "mg/dL"},
    "Calcium": {"min": 8.5, "max": 10.5, "unit": "mg/dL"},
    "Ca": {"min": 8.5, "max": 10.5, "unit": "mg/dL"},
    "마그네슘": {"min": 1.7, "max": 2.3, "unit": "mg/dL"},
    "Magnesium": {"min": 1.7, "max": 2.3, "unit": "mg/dL"},
    "Mg": {"min": 1.7, "max": 2.3, "unit": "mg/dL"},
    
    # 혈액학 (엑셀 파일 참고치 반영)
    "WBC": {"min": 4.2, "max": 10.5, "unit": "ul"},
    "White Blood Cell": {"min": 4.2, "max": 10.5, "unit": "ul"},
    "백혈구": {"min": 4.2, "max": 10.5, "unit": "ul"},
    "백혈구수": {"min": 4.2, "max": 10.5, "unit": "ul"},
    "백혈구수(WBC)": {"min": 4.2, "max": 10.5, "unit": "ul"},
    "RBC": {"min": 4.0, "max": 6.0, "unit": "ul"},
    "Red Blood Cell": {"min": 4.0, "max": 6.0, "unit": "ul"},
    "적혈구": {"min": 4.0, "max": 6.0, "unit": "ul"},
    "적혈구수": {"min": 4.0, "max": 6.0, "unit": "ul"},
    "적혈구수(RBC)": {"min": 4.0, "max": 6.0, "unit": "ul"},
    "Hemoglobin": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "Hgb": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "Hb": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "HB": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "빈혈수치": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "빈혈수치(Hb)": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "혈색소": {"min": 13.5, "max": 18.0, "unit": "g/dl"},
    "Hematocrit": {"min": 35.0, "max": 60.0, "unit": "%"},
    "Hct": {"min": 35.0, "max": 60.0, "unit": "%"},
    "헤마토크릿": {"min": 35.0, "max": 60.0, "unit": "%"},
    "헤마토크리트": {"min": 35.0, "max": 60.0, "unit": "%"},
    "헤마토크리트(Hct)": {"min": 35.0, "max": 60.0, "unit": "%"},
    "Platelet": {"min": 150.0, "max": 450.0, "unit": "ul"},
    "PLT": {"min": 150.0, "max": 450.0, "unit": "ul"},
    "혈소판": {"min": 150.0, "max": 450.0, "unit": "ul"},
    "혈소판수": {"min": 150.0, "max": 450.0, "unit": "ul"},
    "혈소판수(PLT)": {"min": 150.0, "max": 450.0, "unit": "ul"},
    "MCV": {"min": 80.0, "max": 99.9, "unit": "fl"},
    "MCH": {"min": 27.0, "max": 31.0, "unit": "pg"},
    "MCHC": {"min": 33.0, "max": 37.0, "unit": "g/dl"},
    "Diff Count": {"value": "", "unit": ""},
    "Seg.Neutrophil": {"min": 40.0, "max": 75.0, "unit": ""},
    "Segment neutrophil": {"min": 40.0, "max": 75.0, "unit": ""},
    "Segment Neutrophil": {"min": 40.0, "max": 75.0, "unit": ""},
    "Lymphocyte": {"min": 20.0, "max": 45.0, "unit": ""},
    "Monocyte": {"min": 0.0, "max": 10.0, "unit": ""},
    "Eosinophil": {"min": 0.0, "max": 6.0, "unit": ""},
    "Basophil": {"min": 0.0, "max": 2.0, "unit": ""},
    
    # 갑상선
    "TSH": {"min": 0.4, "max": 4.0, "unit": "μIU/mL"},
    "Thyroid Stimulating Hormone": {"min": 0.4, "max": 4.0, "unit": "μIU/mL"},
    "Free T4": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
    "FT4": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
    "Free Thyroxine": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
    "Free T3": {"min": 2.3, "max": 4.2, "unit": "pg/mL"},
    "FT3": {"min": 2.3, "max": 4.2, "unit": "pg/mL"},
    
    # 소변 검사
    # 요일반검사 항목들
    "Leukocyte esterase": {"value": "Negative", "unit": ""},
    "Leukocyte": {"min": 1.003, "max": 1.035, "unit": ""},
    "Nitrite": {"value": "Negative", "unit": ""},
    "아질산염": {"value": "Negative", "unit": ""},
    "Protein": {"value": "Negative", "unit": ""},
    "단백": {"value": "Negative", "unit": ""},
    "Urine Protein": {"value": "Negative", "unit": ""},
    "U-Protein": {"value": "Negative", "unit": ""},
    "단백뇨": {"value": "Negative", "unit": ""},
    "요단백": {"value": "Negative", "unit": ""},
    "Glucose": {"min": 5.0, "max": 8.5, "unit": ""},
    "당": {"value": "Negative", "unit": ""},
    "Urine Glucose": {"value": "Negative", "unit": ""},
    "U-Glucose": {"value": "Negative", "unit": ""},
    "당뇨": {"value": "Negative", "unit": ""},
    "요당": {"value": "Negative", "unit": ""},
    "Ketone": {"value": "Negative", "unit": ""},
    "케톤": {"value": "Negative", "unit": ""},
    "케톤체": {"value": "Negative", "unit": ""},
    "Urobilinogen": {"value": "Trace", "unit": ""},  # Trace는 정상
    "유로빌리노겐": {"value": "Trace", "unit": ""},
    "Bilirubin": {"value": "Negative", "unit": ""},
    "빌리루빈": {"value": "Negative", "unit": ""},
    "요빌리루빈": {"value": "Negative", "unit": ""},
    "Blood": {"value": "Negative", "unit": ""},
    "잠혈": {"value": "Negative", "unit": ""},
    "Urine Blood": {"value": "Negative", "unit": ""},
    "U-Blood": {"value": "Negative", "unit": ""},
    "요잠혈": {"value": "Negative", "unit": ""},
    "Occult Blood": {"value": "Negative", "unit": ""},
    "pH": {"min": 5.0, "max": 8.5, "unit": ""},
    "Urine pH": {"min": 5.0, "max": 8.5, "unit": ""},
    "수소이온농도": {"min": 5.0, "max": 8.5, "unit": ""},
    "Specific Gravity": {"min": 1.003, "max": 1.035, "unit": ""},
    "S.G": {"min": 1.003, "max": 1.035, "unit": ""},
    "비중": {"min": 1.003, "max": 1.035, "unit": ""},
    # 요침사검사 항목들
    "RBC": {"min": 0, "max": 2, "unit": "H.P.F"},
    "적혈구": {"min": 0, "max": 2, "unit": "H.P.F"},
    "WBC": {"min": 0, "max": 2, "unit": "H.P.F"},
    "백혈구": {"min": 0, "max": 2, "unit": "H.P.F"},
    "Epi.cell": {"min": 0, "max": 2, "unit": "H.P.F"},
    "Epithelial cell": {"min": 0, "max": 2, "unit": "H.P.F"},
    "상피세포": {"min": 0, "max": 2, "unit": "H.P.F"},
    "Casts": {"value": "Not Found", "unit": "L.P.F"},
    "원주": {"value": "Not Found", "unit": "L.P.F"},
    "Cast": {"value": "Not Found", "unit": "L.P.F"},
    "bacteria": {"value": "Not Found", "unit": "H.P.F"},
    "Bacteria": {"value": "Not Found", "unit": "H.P.F"},
    "세균": {"value": "Not Found", "unit": "H.P.F"},
    "Crystals": {"value": "Not Found", "unit": "H.P.F"},
    "결정체": {"value": "Not Found", "unit": "H.P.F"},
    "결정": {"value": "Not Found", "unit": "H.P.F"},
    "Others": {"value": "Not Found", "unit": "H.P.F"},
    "기타": {"value": "Not Found", "unit": "H.P.F"},
}


def find_test_group(test_name):
    """검사 항목명으로 그룹 찾기"""
    import re
    
    # 1단계: 정확한 매칭 시도 (대소문자 무시)
    for group_key, group_info in TEST_GROUPS.items():
        for test in group_info["tests"]:
            if test.lower() == test_name.lower():
                return group_key
    
    # 2단계: 단어 경계를 고려한 매칭
    for group_key, group_info in TEST_GROUPS.items():
        for test in group_info["tests"]:
            # test가 test_name에 완전한 단어로 포함되는지 확인
            pattern = r'\b' + re.escape(test.lower()) + r'\b'
            if re.search(pattern, test_name.lower()):
                return group_key
    
    # 3단계: 부분 문자열 매칭 (fallback)
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
        # 값 전처리 (특수 기호 제거)
        value_str = str(value).strip()
        
        # 특수 기호가 있으면 이상으로 판단
        if any(symbol in value_str for symbol in ['▲', '▼', '↑', '↓']):
            return True
        
        # 수치형 비교
        if "min" in ref_range and "max" in ref_range:
            # 숫자만 추출
            import re
            value_clean = re.sub(r'[^0-9.]', '', value_str)
            if not value_clean:
                return False
            value_num = float(value_clean)
            return value_num < ref_range["min"] or value_num > ref_range["max"]
        
        # 문자형 비교 (Negative 등)
        if "value" in ref_range:
            value_lower = value_str.lower()
            ref_lower = str(ref_range["value"]).lower()
            # - 또는 negative는 정상
            if value_lower in ['-', 'negative', 'neg']:
                return ref_lower not in ['-', 'negative', 'neg']
            # + 또는 positive는 이상
            if value_lower in ['+', 'positive', 'pos', 'trace']:
                return True
            return value_lower != ref_lower
    except (ValueError, TypeError):
        return False
    
    return False


def get_abnormal_direction(test_name, value):
    """이상 방향 (높음/낮음) 판별"""
    ref_range = get_reference_range(test_name)
    if not ref_range or "min" not in ref_range:
        return None
    
    try:
        # 특수 기호 확인
        value_str = str(value).strip()
        if '▲' in value_str or '↑' in value_str:
            return "high"
        if '▼' in value_str or '↓' in value_str:
            return "low"
        
        # 숫자만 추출
        import re
        value_clean = re.sub(r'[^0-9.]', '', value_str)
        if not value_clean:
            return None
        
        value_num = float(value_clean)
        if value_num < ref_range["min"]:
            return "low"
        elif value_num > ref_range["max"]:
            return "high"
    except (ValueError, TypeError):
        pass
    
    return None
