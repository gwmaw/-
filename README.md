# 의료 검사 리포트 생성기

## 프로젝트 개요
환자의 의료 검사 결과(혈액검사, 소변검사 등)를 엑셀 파일에서 읽어 자동으로 분석하고, 모바일 친화적인 PDF/PNG 리포트를 생성하는 웹 애플리케이션입니다.

## 주요 기능
- ✅ **실제 병원 검체검사결과 파일 지원** (처방명, 참고치, 날짜 컬럼)
- ✅ 엑셀 파일에서 검사 결과 자동 추출
- ✅ 환자명 자동 추출 (파일명에서)
- ✅ 검사 항목 자동 그룹화 (간기능, 신기능, 당뇨, 지질 등)
- ✅ 정상/이상 범위 자동 판별 및 시각화
- ✅ 특수 기호 자동 감지 (▲, ▼)
- ✅ 의료진 코멘트 입력 기능
- ✅ 모바일 최적화된 세로형 리포트
- ✅ HTML 및 PDF 형식으로 출력

## 검사 항목 그룹

### 1. 간기능 검사
- AST(SGOT), ALT(SGPT), GGT
- Total Bilirubin, ALP

### 2. 신기능 검사
- BUN, Creatinine, eGFR
- Uric Acid

### 3. 당뇨 검사
- Glucose (공복혈당), HbA1c

### 4. 지질 검사
- Total Cholesterol, LDL, HDL, Triglyceride

### 5. 혈액학 검사
- WBC, RBC, Hemoglobin, Hematocrit
- Platelet

### 6. 갑상선 검사
- TSH, Free T4, Free T3

### 7. 소변 검사
- Protein, Glucose, Blood, pH

## 설치 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python src/app.py
```

## 사용 방법

1. 웹 브라우저에서 `http://localhost:5000` 접속
2. 엑셀 파일 업로드 (검사 결과 포함)
3. 의료진 코멘트 입력
4. **PDF** 또는 **HTML**로 다운로드

### 📄 출력 형식 안내

#### PDF (권장)
- 한글 완벽 지원 (WeasyPrint 사용)
- 인쇄 및 공유에 최적화
- 파일 크기: 약 50-70KB

#### HTML
- 브라우저에서 즉시 확인
- PDF로 인쇄 가능 (Ctrl+P 또는 Cmd+P)
- 가장 깨끗한 한글 표시
- **추천**: HTML을 브라우저에서 열어 PDF로 인쇄하면 최상의 품질

## 엑셀 파일 형식

### 형식 1: 표준 형식
엑셀 파일은 다음 열을 포함해야 합니다:
- 검사항목명 (Test Name)
- 검사결과값 (Result)
- 단위 (Unit)
- 정상범위 (Reference Range) - 선택사항

예시:
```
검사항목명      | 결과    | 단위   | 정상범위
AST(SGOT)     | 45      | U/L    | 0-40
ALT(SGPT)     | 52      | U/L    | 0-40
Total Chol    | 220     | mg/dL  | 0-200
```

### 형식 2: 병원 검체검사결과 형식 (⭐ 지원됨)
실제 병원에서 발급하는 검체검사결과 파일 형식을 지원합니다:
- **처방명** (검사 항목)
- **참고치** (정상 범위)
- **단위**
- **날짜** (예: 2026-01-20) - 결과값이 날짜 컬럼에 위치

예시:
```
처방명          | 참고치      | 단위   | 2026-01-20
간기능(AST)     | 0 ~ 40     | U/L    | 25
간기능(ALT)     | 0 ~ 40     | U/L    | 24
총콜레스테롤     | 0 ~ 199    | mg/dl  | 155
```

**특수 기호 자동 처리:**
- `▲` 또는 `186(▲)`: 정상 범위보다 높음
- `▼`: 정상 범위보다 낮음
- `+`: 양성 (이상)
- `-`: 음성 (정상)

**파일명 규칙:**
- 환자명이 파일명 앞에 있으면 자동 추출됩니다
- 예: `김수미_검체검사결과_20260121.xlsx` → 환자명: 김수미

## 프로젝트 구조

```
/home/user/webapp/
├── src/
│   ├── app.py                    # Flask 메인 애플리케이션
│   ├── test_definitions.py       # 검사 항목 정의 및 정상 범위
│   ├── excel_parser.py           # 엑셀 파일 파싱
│   ├── report_analyzer.py        # 검사 결과 분석
│   ├── report_generator.py       # 리포트 생성
│   ├── templates/
│   │   ├── index.html           # 업로드 페이지
│   │   └── report_template.html # 리포트 템플릿
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── uploads/                      # 업로드된 엑셀 파일
├── output/                       # 생성된 리포트
├── requirements.txt
└── README.md
```

## 기술 스택
- **Backend**: Flask (Python)
- **Excel Processing**: pandas, openpyxl
- **PDF Generation**: WeasyPrint
- **Image Generation**: Pillow
- **Visualization**: matplotlib

## 모바일 최적화
- 세로형 A4 비율 (210mm × 297mm)
- 터치 친화적 UI
- 스크롤 최적화
- 큰 글씨 및 명확한 색상 구분

## 라이선스
MIT License
