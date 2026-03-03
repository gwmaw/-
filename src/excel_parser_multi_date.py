"""
다중 날짜 엑셀 파일 파싱 모듈
하나의 엑셀 파일에서 여러 날짜의 검사 결과를 추출
"""

import pandas as pd
import re
from datetime import datetime


def parse_multi_date_excel(file_path):
    """
    다중 날짜 엑셀 파일 파싱
    
    Args:
        file_path: 엑셀 파일 경로
    
    Returns:
        dict: {
            'dates': [날짜 리스트 (최신순)],
            'date_columns': [날짜별 컬럼명],
            'tests_by_date': {날짜: [검사 결과 리스트]},
            'patient_info': 환자 정보
        }
    """
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, sheet_name=0)
        df.columns = [str(col).strip() for col in df.columns]
        
        # 날짜 컬럼 찾기 (YYYY-MM-DD 형식)
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        date_columns = []
        dates = []
        
        for col in df.columns:
            if re.match(date_pattern, str(col)):
                date_columns.append(col)
                try:
                    date_obj = datetime.strptime(col, '%Y-%m-%d')
                    dates.append((col, date_obj))
                except:
                    pass
        
        # 날짜 정렬 (최신순)
        dates.sort(key=lambda x: x[1], reverse=True)
        date_columns_sorted = [d[0] for d in dates]
        
        if len(date_columns_sorted) == 0:
            # 날짜 컬럼이 없으면 기존 단일 결과 방식
            return None
        
        print(f"📅 발견된 날짜: {len(date_columns_sorted)}개")
        print(f"   최신: {date_columns_sorted[0] if date_columns_sorted else 'N/A'}")
        print(f"   가장 오래된: {date_columns_sorted[-1] if date_columns_sorted else 'N/A'}")
        
        # 각 날짜별 검사 결과 추출
        tests_by_date = {}
        
        for date_col in date_columns_sorted:
            tests = _extract_tests_for_date(df, date_col)
            if tests:
                tests_by_date[date_col] = tests
        
        # 환자 정보 추출 (파일명에서)
        patient_info = _extract_patient_info_from_filename(file_path)
        
        return {
            'dates': date_columns_sorted,
            'date_columns': date_columns_sorted,
            'tests_by_date': tests_by_date,
            'patient_info': patient_info
        }
        
    except Exception as e:
        print(f"❌ 다중 날짜 파싱 실패: {e}")
        return None


def _extract_tests_for_date(df, date_col):
    """특정 날짜의 검사 결과 추출"""
    tests = []
    
    # 컬럼 찾기
    test_name_col = _find_column(df, ['검사항목', '항목', 'test', 'name', '검사명', 'item', '처방명', '처방'])
    ref_col = _find_column(df, ['정상범위', '참고치', 'reference', 'ref', 'range', 'normal'])
    unit_col = df.columns[2] if len(df.columns) > 2 else None
    
    if test_name_col is None:
        return tests
    
    # 소변검사 섹션 플래그
    in_urine_section = False
    in_urine_sediment_section = False
    
    for idx, row in df.iterrows():
        test_name = str(row[test_name_col]).strip()
        result_value = row[date_col]
        
        # 빈 행 건너뛰기
        if pd.isna(test_name) or test_name == '' or test_name.lower() in ['nan', 'none']:
            continue
        
        # 소변검사 섹션 감지
        if '요 일반검사' in test_name or '요일반검사' in test_name or '소변검사' in test_name:
            in_urine_section = True
            continue
        elif '요침사검사' in test_name:
            in_urine_sediment_section = True
            in_urine_section = False
            continue
        
        # NaN이거나 빈 결과는 건너뛰기 (해당 날짜에 검사하지 않음)
        if pd.isna(result_value):
            continue
        
        result_value = str(result_value).strip()
        if result_value == '' or result_value.lower() == 'nan':
            continue
        
        # 화살표 및 기호 제거
        result_cleaned = result_value.replace('▲', '').replace('▼', '').replace('(', '').replace(')', '').replace('c', '').strip()
        
        # 단위 추출
        unit = ''
        if unit_col and not pd.isna(row[unit_col]):
            unit = str(row[unit_col]).strip()
        
        # 참고치 추출
        reference = ''
        if ref_col and not pd.isna(row[ref_col]):
            reference = str(row[ref_col]).strip()
        
        # 검사 데이터 구성
        test_data = {
            'name': test_name,
            'result': result_cleaned,
            'original_result': result_value,
            'unit': unit,
            'reference': reference
        }
        
        # 소변검사 카테고리 힌트
        if in_urine_section or in_urine_sediment_section:
            test_data['category_hint'] = 'urine'
        
        tests.append(test_data)
    
    return tests


def _find_column(df, keywords):
    """키워드로 컬럼 찾기"""
    for col in df.columns:
        col_lower = str(col).lower()
        for keyword in keywords:
            if keyword.lower() in col_lower:
                return col
    return None


def _extract_patient_info_from_filename(file_path):
    """파일명에서 환자 정보 추출"""
    import os
    filename = os.path.basename(file_path)
    
    # 파일명 패턴: 이름_검체검사결과_날짜.xlsx
    match = re.match(r'([^_]+)_검체검사결과_(\d{8})', filename)
    
    patient_info = {
        'name': '',
        'id': '',
        'age': '',
        'gender': '',
        'date': ''
    }
    
    if match:
        patient_info['name'] = match.group(1)
        date_str = match.group(2)  # YYYYMMDD
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            patient_info['date'] = date_obj.strftime('%Y-%m-%d')
        except:
            pass
    
    return patient_info


def get_latest_and_previous_tests(multi_date_data, min_test_count=10):
    """
    최신 검사와 이전 검사 추출
    
    Args:
        multi_date_data: parse_multi_date_excel의 반환값
        min_test_count: 유효한 검사로 간주할 최소 항목 수 (기본값: 10)
    
    Returns:
        tuple: (current_tests, previous_tests) 또는 (current_tests, None)
    """
    if not multi_date_data or 'dates' not in multi_date_data:
        return None, None
    
    dates = multi_date_data['dates']
    tests_by_date = multi_date_data['tests_by_date']
    
    if len(dates) == 0:
        return None, None
    
    # 최신 검사
    current_date = dates[0]
    current_tests = tests_by_date.get(current_date, [])
    
    # 이전 검사 찾기 (충분한 항목이 있는 날짜)
    previous_tests = None
    previous_date = None
    
    for date in dates[1:]:
        tests = tests_by_date.get(date, [])
        if len(tests) >= min_test_count:
            previous_tests = tests
            previous_date = date
            break
    
    if previous_date:
        print(f"✅ 이전 검사 선택: {previous_date} ({len(previous_tests)}개 항목)")
    
    return current_tests, previous_tests
