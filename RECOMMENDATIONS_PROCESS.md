# 🔍 권장사항 생성 프로세스 상세 설명

## 📋 개요

현재 시스템의 **권장사항(Recommendations)**은 **규칙 기반(Rule-Based)** 방식으로 생성됩니다.  
**AI나 LLM(GPT 등)을 사용하지 않고**, 사전에 정의된 규칙과 조건에 따라 자동으로 권장사항을 제공합니다.

---

## 🔄 권장사항 생성 과정 (4단계)

### 1단계: 엑셀 파일 파싱
📁 **파일**: `src/excel_parser.py`

```python
# 엑셀 파일에서 검사 항목 추출
parsed_data = parse_excel_file(file_path)
# 결과: {'tests': [...], 'patient_info': {...}}
```

**출력 예시**:
```python
{
    'tests': [
        {'name': '당화혈색소(HbA1c)', 'result': '6.4', 'unit': '%', 'reference': '4.5 ~ 5.6'},
        {'name': '총콜레스테롤', 'result': '139', 'unit': 'mg/dl', 'reference': '0 - 199'},
        # ... 32개 항목
    ],
    'patient_info': {'name': '전성우', 'date': '2026-01-21'}
}
```

---

### 2단계: 검사 결과 분석 및 이상 판별
📁 **파일**: `src/report_analyzer.py`

#### 2-1. 카테고리별 분류
```python
# test_definitions.py의 TEST_GROUPS를 기반으로 분류
grouped_tests = {
    'liver': [...],      # 간기능 검사
    'kidney': [...],     # 신기능 검사
    'diabetes': [...],   # 당뇨 검사
    'lipid': [...],      # 지질 검사
    'blood': [...],      # 혈액학 검사
    # ...
}
```

#### 2-2. 이상 여부 판별
```python
def is_abnormal(test_name, result):
    """참고치와 비교하여 이상 여부 판별"""
    ref_range = get_reference_range(test_name)  # test_definitions.py에서 참고치 가져오기
    
    if ref_range:
        if 'min' in ref_range and 'max' in ref_range:
            # 숫자형 결과
            try:
                result_num = float(result)
                if result_num < ref_range['min'] or result_num > ref_range['max']:
                    return True  # 이상
            except:
                pass
        elif 'value' in ref_range:
            # 텍스트형 결과 (예: Negative)
            if result != ref_range['value']:
                return True  # 이상
    
    return False  # 정상
```

**판별 예시**:
| 검사명 | 결과 | 참고치 | 이상 여부 |
|--------|------|--------|-----------|
| 당화혈색소(HbA1c) | 6.4% | 4.5 ~ 5.6% | ✅ 이상 (높음) |
| 총콜레스테롤 | 139 mg/dl | 0 ~ 199 mg/dl | ⭕ 정상 |
| 고밀도콜레스테롤(HDL) | 48 mg/dl | 60 ~ 999 mg/dl | ✅ 이상 (낮음) |

#### 2-3. 이상 항목 집계
```python
abnormal_tests = [
    {'group': '당뇨 검사', 'test': {...}},     # 당화혈색소 6.4%
    {'group': '당뇨 검사', 'test': {...}},     # 혈당검사 107
    {'group': '지질 검사', 'test': {...}},     # HDL 48
    {'group': '지질 검사', 'test': {...}},     # 중성지방 161
    {'group': '전해질 검사', 'test': {...}},   # 칼륨 7.5
]
```

---

### 3단계: 권장사항 생성 (핵심!)
📁 **파일**: `src/report_analyzer.py` - `get_recommendations()` 메서드

#### 3-1. 사전 정의된 그룹별 권장사항
```python
group_recommendations = {
    'liver': '간기능 이상이 관찰되었습니다. 음주를 자제하고 규칙적인 운동과 균형잡힌 식사를 권장합니다.',
    'kidney': '신기능 이상이 관찰되었습니다. 충분한 수분 섭취와 저염식을 권장합니다.',
    'diabetes': '혈당 조절이 필요합니다. 규칙적인 식사와 운동, 체중 관리를 권장합니다.',
    'lipid': '지질 관리가 필요합니다. 저지방 식단과 규칙적인 운동을 권장합니다.',
    'blood': '혈액학적 이상이 관찰되었습니다. 추가 검사가 필요할 수 있습니다.',
    'thyroid': '갑상선 기능 이상이 관찰되었습니다. 전문의 상담을 권장합니다.',
    'urine': '소변 검사 이상이 관찰되었습니다. 추가 검사가 필요할 수 있습니다.'
}
```

#### 3-2. 권장사항 선택 로직
```python
def get_recommendations(self):
    recommendations = []
    abnormal_tests = self.get_abnormal_tests()  # 이상 항목 가져오기
    
    # 이상 소견이 있는 그룹의 권장사항 추가
    added_groups = set()
    for item in abnormal_tests:
        group_key = find_test_group(item['test']['name'])  # 어느 그룹인지 찾기
        if group_key and group_key not in added_groups:
            if group_key in group_recommendations:
                recommendations.append(group_recommendations[group_key])
                added_groups.add(group_key)
    
    # 이상 소견이 없으면 일반 권장사항
    if not recommendations:
        recommendations.append('모든 검사 결과가 정상 범위 내에 있습니다. 건강한 생활습관을 유지하시기 바랍니다.')
    
    return recommendations
```

#### 3-3. 실제 생성 예시
**입력**: 이상 항목
- 당화혈색소(HbA1c): 6.4% ↑ → `diabetes` 그룹
- 혈당검사: 107 mg/dl ↑ → `diabetes` 그룹
- 고밀도콜레스테롤(HDL): 48 mg/dl ↓ → `lipid` 그룹
- 중성지방(TG): 161 mg/dl ↑ → `lipid` 그룹
- 칼륨: 7.5 mmol/L ↑ → `electrolyte` 그룹

**중간 과정**:
1. `diabetes` 그룹 발견 → 권장사항 추가
2. `diabetes` 그룹 또 발견 → 이미 추가됨 (중복 제거)
3. `lipid` 그룹 발견 → 권장사항 추가
4. `lipid` 그룹 또 발견 → 이미 추가됨 (중복 제거)
5. `electrolyte` 그룹 발견 → **권장사항 없음** (정의되지 않음)

**출력**: 권장사항 목록
```python
recommendations = [
    '혈당 조절이 필요합니다. 규칙적인 식사와 운동, 체중 관리를 권장합니다.',
    '지질 관리가 필요합니다. 저지방 식단과 규칙적인 운동을 권장합니다.'
]
```

---

### 4단계: PDF 리포트 생성
📁 **파일**: `src/report_generator.py`, `src/templates/report_template.html`

```python
# 권장사항을 템플릿에 전달
output_file = generate_report(
    analysis_data={
        'recommendations': [
            '혈당 조절이 필요합니다. 규칙적인 식사와 운동, 체중 관리를 권장합니다.',
            '지질 관리가 필요합니다. 저지방 식단과 규칙적인 운동을 권장합니다.'
        ]
    },
    ...
)
```

**PDF 출력**:
```
┌─────────────────────────────────────┐
│  💡 권장사항                        │
├─────────────────────────────────────┤
│  • 혈당 조절이 필요합니다.          │
│    규칙적인 식사와 운동,            │
│    체중 관리를 권장합니다.          │
│                                     │
│  • 지질 관리가 필요합니다.          │
│    저지방 식단과 규칙적인 운동을    │
│    권장합니다.                      │
└─────────────────────────────────────┘
```

---

## 🔧 사용된 기술 및 도구

### ❌ 사용하지 않는 것
- ❌ **AI/머신러닝**: 사용하지 않음
- ❌ **LLM (GPT, Claude 등)**: 사용하지 않음
- ❌ **자연어 처리(NLP)**: 사용하지 않음
- ❌ **외부 API**: 사용하지 않음

### ✅ 사용하는 것
- ✅ **규칙 기반 시스템** (Rule-Based System)
- ✅ **Python 표준 라이브러리**
- ✅ **조건문 (if-else)** 및 **딕셔너리**
- ✅ **사전 정의된 참고치** (`test_definitions.py`)
- ✅ **그룹별 권장사항 매핑** (Dictionary)

---

## 🎯 장점 및 단점

### ✅ 장점
1. **빠른 응답 속도** - 복잡한 계산 없이 즉시 생성
2. **비용 효율적** - API 호출 비용 없음
3. **일관성** - 동일한 입력에 항상 동일한 출력
4. **투명성** - 로직이 명확하고 추적 가능
5. **오프라인 작동** - 인터넷 연결 불필요

### ❌ 단점
1. **유연성 부족** - 새로운 상황에 대응 어려움
2. **개인화 불가** - 환자 개인별 맞춤 권장사항 불가
3. **복합 소견 처리 한계** - 여러 이상이 복합적일 때 단순 나열
4. **업데이트 필요** - 의학 지식 변경 시 수동 수정 필요

---

## 🔄 개선 방안 (향후 가능한 방향)

### 1️⃣ 상세 규칙 추가
```python
# 현재: 그룹별 단일 권장사항
'diabetes': '혈당 조절이 필요합니다. ...'

# 개선: 수치별 세분화
'diabetes': {
    'mild': 'HbA1c가 약간 높습니다. 식이요법과 운동으로 개선 가능합니다.',
    'moderate': 'HbA1c가 높습니다. 전문의 상담과 생활습관 개선이 필요합니다.',
    'severe': 'HbA1c가 매우 높습니다. 즉시 전문의 상담이 필요합니다.'
}
```

### 2️⃣ 복합 소견 처리
```python
# 당뇨 + 지질 이상 동시 발생 시
if 'diabetes' in abnormal_groups and 'lipid' in abnormal_groups:
    recommendations.append('당뇨와 고지혈증이 함께 관찰되었습니다. 심혈관 질환 위험이 높으므로...')
```

### 3️⃣ LLM 통합 (선택적)
```python
# OpenAI GPT API를 사용한 개인화 권장사항
def generate_ai_recommendations(abnormal_tests, patient_info):
    prompt = f"""
    환자: {patient_info['name']}, 나이: {patient_info['age']}, 성별: {patient_info['gender']}
    이상 소견: {abnormal_tests}
    
    위 검사 결과를 바탕으로 환자에게 맞춤형 권장사항을 3가지 제시해주세요.
    """
    response = openai.ChatCompletion.create(model="gpt-4", messages=[...])
    return response['choices'][0]['message']['content']
```

### 4️⃣ 전문의 지식 베이스 구축
```python
# 의학 전문가가 작성한 세분화된 권장사항 DB
recommendations_db = {
    'HbA1c_6.0_6.5': '당뇨 전단계입니다. 지금부터 생활습관 개선이 중요합니다...',
    'HbA1c_6.5_7.0': '당뇨로 진단됩니다. 전문의 상담이 필요하며...',
    'HbA1c_7.0_plus': '혈당 조절이 시급합니다. 즉시 전문의를 방문하세요...'
}
```

---

## 📝 요약

### 현재 시스템
```
엑셀 파일 → 파싱 → 이상 판별 → 그룹별 권장사항 매칭 → PDF 생성
              ↓        ↓              ↓
         Python   참고치 비교    사전 정의된 텍스트
```

### 사용 도구
- **언어**: Python 3
- **라이브러리**: pandas, openpyxl (엑셀 파싱)
- **방식**: 규칙 기반 (Rule-Based)
- **AI/LLM**: 사용하지 않음

### 권장사항 생성 핵심
**"이상이 발견된 검사 카테고리에 매핑된 고정 텍스트를 반환"**

---

## 💡 결론

현재 시스템은 **간단하고 효율적인 규칙 기반 방식**으로 작동합니다.  
의학적으로 검증된 일반적인 권장사항을 제공하지만,  
**개인화된 상세 권장사항이 필요하다면 LLM 통합을 고려**할 수 있습니다.

---

**문의사항이 있으시면 언제든지 말씀해주세요!** 🚀
