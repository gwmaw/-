"""
샘플 엑셀 데이터 생성 스크립트
테스트용 검사 결과 데이터 생성
"""

import pandas as pd
import os
from datetime import datetime

def create_sample_data():
    """샘플 검사 결과 데이터 생성"""
    
    # 정상 범위의 샘플 데이터
    normal_data = [
        # 간기능
        ['AST(SGOT)', 28, 'U/L', '0-40'],
        ['ALT(SGPT)', 32, 'U/L', '0-40'],
        ['GGT', 35, 'U/L', '0-60'],
        ['Total Bilirubin', 0.8, 'mg/dL', '0.2-1.2'],
        ['ALP', 85, 'U/L', '30-120'],
        
        # 신기능
        ['BUN', 15, 'mg/dL', '8-20'],
        ['Creatinine', 0.9, 'mg/dL', '0.6-1.2'],
        ['eGFR', 95, 'mL/min/1.73m²', '>90'],
        ['Uric Acid', 5.2, 'mg/dL', '3.5-7.0'],
        
        # 당뇨
        ['Glucose', 92, 'mg/dL', '70-100'],
        ['HbA1c', 5.2, '%', '4.0-5.6'],
        
        # 지질
        ['Total Cholesterol', 185, 'mg/dL', '0-200'],
        ['LDL', 110, 'mg/dL', '0-130'],
        ['HDL', 55, 'mg/dL', '>40'],
        ['Triglyceride', 120, 'mg/dL', '0-150'],
        
        # 혈액학
        ['WBC', 6.5, '10³/μL', '4.0-10.0'],
        ['RBC', 4.8, '10⁶/μL', '4.2-6.0'],
        ['Hemoglobin', 14.5, 'g/dL', '12.0-18.0'],
        ['Hematocrit', 42, '%', '37.0-52.0'],
        ['Platelet', 250, '10³/μL', '150-400'],
        
        # 갑상선
        ['TSH', 2.1, 'μIU/mL', '0.4-4.0'],
        ['Free T4', 1.2, 'ng/dL', '0.8-1.8'],
        
        # 소변
        ['Urine Protein', 'Negative', '', 'Negative'],
        ['Urine Glucose', 'Negative', '', 'Negative'],
        ['Urine Blood', 'Negative', '', 'Negative'],
        ['pH', 6.5, '', '5.0-8.0'],
    ]
    
    # 이상 소견이 있는 샘플 데이터
    abnormal_data = [
        # 간기능 - 일부 높음
        ['AST(SGOT)', 52, 'U/L', '0-40'],
        ['ALT(SGPT)', 68, 'U/L', '0-40'],
        ['GGT', 85, 'U/L', '0-60'],
        ['Total Bilirubin', 1.5, 'mg/dL', '0.2-1.2'],
        ['ALP', 95, 'U/L', '30-120'],
        
        # 신기능 - 정상
        ['BUN', 18, 'mg/dL', '8-20'],
        ['Creatinine', 1.0, 'mg/dL', '0.6-1.2'],
        ['eGFR', 92, 'mL/min/1.73m²', '>90'],
        ['Uric Acid', 6.8, 'mg/dL', '3.5-7.0'],
        
        # 당뇨 - 경계
        ['Glucose', 108, 'mg/dL', '70-100'],
        ['HbA1c', 5.9, '%', '4.0-5.6'],
        
        # 지질 - 높음
        ['Total Cholesterol', 245, 'mg/dL', '0-200'],
        ['LDL', 158, 'mg/dL', '0-130'],
        ['HDL', 42, 'mg/dL', '>40'],
        ['Triglyceride', 185, 'mg/dL', '0-150'],
        
        # 혈액학 - 정상
        ['WBC', 7.2, '10³/μL', '4.0-10.0'],
        ['RBC', 4.6, '10⁶/μL', '4.2-6.0'],
        ['Hemoglobin', 13.8, 'g/dL', '12.0-18.0'],
        ['Hematocrit', 41, '%', '37.0-52.0'],
        ['Platelet', 220, '10³/μL', '150-400'],
        
        # 갑상선 - 정상
        ['TSH', 2.5, 'μIU/mL', '0.4-4.0'],
        ['Free T4', 1.3, 'ng/dL', '0.8-1.8'],
        
        # 소변 - 일부 이상
        ['Urine Protein', 'Trace', '', 'Negative'],
        ['Urine Glucose', 'Negative', '', 'Negative'],
        ['Urine Blood', 'Negative', '', 'Negative'],
        ['pH', 7.2, '', '5.0-8.0'],
    ]
    
    return normal_data, abnormal_data


def save_sample_excel(data, filename):
    """샘플 데이터를 엑셀 파일로 저장"""
    df = pd.DataFrame(data, columns=['검사항목명', '결과', '단위', '정상범위'])
    
    # 파일 경로
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # 엑셀 저장
    df.to_excel(filepath, index=False, sheet_name='검사결과')
    
    print(f"✅ 샘플 파일 생성: {filepath}")
    return filepath


if __name__ == '__main__':
    print("=" * 60)
    print("샘플 데이터 생성 중...")
    print("=" * 60)
    
    normal_data, abnormal_data = create_sample_data()
    
    # 정상 범위 샘플
    save_sample_excel(normal_data, 'sample_normal.xlsx')
    
    # 이상 소견 샘플
    save_sample_excel(abnormal_data, 'sample_abnormal.xlsx')
    
    print("=" * 60)
    print("✅ 샘플 데이터 생성 완료!")
    print("=" * 60)
    print("\n생성된 파일:")
    print("  - uploads/sample_normal.xlsx (정상 범위)")
    print("  - uploads/sample_abnormal.xlsx (이상 소견 포함)")
    print("\n웹 인터페이스에서 이 파일들을 업로드하여 테스트하세요.")
