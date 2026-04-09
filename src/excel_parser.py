"""
엑셀 파일 파싱 모듈
다양한 형식의 엑셀 파일에서 검사 결과 추출
"""

import pandas as pd
import re
from pathlib import Path


class ExcelParser:
    """엑셀 파일에서 검사 결과를 추출하는 클래스"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.tests = []
        
    def parse(self):
        """엑셀 파일 파싱"""
        try:
            # 엑셀 파일 읽기 (모든 시트 확인)
            excel_file = pd.ExcelFile(self.file_path)
            
            # 첫 번째 시트부터 데이터 찾기
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                
                # 데이터가 있는 시트 찾기
                if not df.empty:
                    self.data = df
                    break
            
            if self.data is None:
                raise ValueError("엑셀 파일에 데이터가 없습니다.")
            
            # 데이터 추출
            self.tests = self._extract_tests()
            return self.tests
            
        except Exception as e:
            raise Exception(f"엑셀 파일 파싱 오류: {str(e)}")
    
    def _extract_tests(self):
        """검사 결과 데이터 추출"""
        tests = []
        
        # 컬럼명 정규화 (소문자, 공백 제거)
        df = self.data.copy()
        df.columns = [str(col).strip() for col in df.columns]
        
        # 가능한 컬럼명 패턴
        test_name_cols = self._find_column(df, ['검사항목', '항목', 'test', 'name', '검사명', 'item', '처방명', '처방'])
        result_cols = self._find_column(df, ['결과', 'result', 'value', '값', '측정값'])
        
        # 단위는 항상 3번째 열(C열, 인덱스 2)에서 읽기
        unit_cols = df.columns[2] if len(df.columns) > 2 else None
        
        ref_cols = self._find_column(df, ['정상범위', '참고치', 'reference', 'ref', 'range', 'normal'])
        
        # 결과 컬럼이 없으면 날짜 컬럼을 찾기 (YYYY-MM-DD 형식)
        # 가장 왼쪽(최신) 날짜 컬럼 찾기
        if result_cols is None:
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            for col in df.columns:
                if re.match(date_pattern, str(col)):
                    result_cols = col
                    break
        
        if test_name_cols is None:
            raise ValueError("필수 컬럼(검사항목/처방명)을 찾을 수 없습니다.")
        
        if result_cols is None:
            raise ValueError("필수 컬럼(결과/날짜)을 찾을 수 없습니다.")
        
        # 각 행에서 검사 데이터 추출
        in_urine_section = False  # 소변검사 섹션 플래그
        in_urine_sediment_section = False  # 요침사검사 섹션 플래그
        
        for idx, row in df.iterrows():
            test_name = str(row[test_name_cols]).strip()
            result_value = row[result_cols]
            
            # 빈 행이나 헤더 행 건너뛰기
            if pd.isna(test_name) or test_name == '' or test_name.lower() in ['nan', 'none']:
                continue
            
            # 소변검사 섹션 감지
            if '요 일반검사' in test_name or '요일반검사' in test_name or '소변검사' in test_name:
                in_urine_section = True
            elif '요침사검사' in test_name:
                in_urine_sediment_section = True
                in_urine_section = False  # 요침사로 전환
            
            # 결과값 정리
            if pd.isna(result_value):
                result_value = ''
            else:
                result_value = str(result_value).strip()
            
            # 🚨 최신 검사일에 결과값이 없으면 이 검사를 제외
            if not result_value or result_value == '' or result_value.lower() == 'nan':
                continue  # 이 검사는 리포트에 포함하지 않음
            
            # 특수 기호 제거 및 처리 (▲, ▼ 등)
            original_result = result_value
            result_clean = re.sub(r'[▲▼()（）]', '', result_value).strip()
            
            # 단위 추출
            unit = ''
            if unit_cols is not None and not pd.isna(row[unit_cols]):
                unit = str(row[unit_cols]).strip()
                # NaN 문자열 제거
                if unit.lower() == 'nan':
                    unit = ''
            
            # 정상범위 추출
            reference = ''
            if ref_cols is not None and not pd.isna(row[ref_cols]):
                reference = str(row[ref_cols]).strip()
                # NaN 문자열 제거
                if reference.lower() == 'nan':
                    reference = ''
            
            # 🔧 간기능(γ-GTP) 참고치 수정: 11 ~ 61
            if 'γ-GTP' in test_name or 'GTP' in test_name.upper():
                reference = '11 ~ 61'
            
            # 특정 항목의 긴 결과값 정리
            # 1. 백혈구백분율: 결과값이 세부 항목들로 구성되어 있으면 제거
            if '백혈구백분율' in test_name:
                # 세부 항목들이 아래에 있으므로 이 항목은 빈 결과로 표시하지 않음
                result_clean = ''
                result_value = ''
            
            # 2. 요일반검사: 결과값이 길면 제거 (세부 항목들이 아래에 있음)
            if '요 일반검사' in test_name or '요일반검사' in test_name or '소변검사' in test_name:
                result_clean = ''
                result_value = ''
            
            # 3. 요침사검사: 결과값이 길면 제거 (세부 항목들이 아래에 있음)
            if '요침사검사' in test_name:
                result_clean = ''
                result_value = ''
            
            # 4. HbA1c 관련 항목 필터링
            # HbA1c-IFCC, HbA1c-eAG, 헤모글로빈A1C 항목은 제외
            skip_tests = [
                'HbA1c-IFCC', 'HbA1c-eAG', 
                '헤모글로빈A1C', 'Hemoglobin A1C'
            ]
            
            should_skip = False
            for skip_term in skip_tests:
                if skip_term.lower() in test_name.lower():
                    # 단, HbA1c-NGSP는 포함
                    if 'NGSP' not in test_name:
                        should_skip = True
                        break
            
            if should_skip:
                continue  # 이 항목은 건너뜀
            
            # 검사 데이터 저장
            test = {
                'name': test_name,
                'result': result_clean if result_clean else result_value,
                'unit': unit,
                'reference': reference,
                'original_result': original_result  # 원본 결과 저장
            }
            
            # 소변검사 섹션에 있으면 category_hint 추가
            if in_urine_section or in_urine_sediment_section:
                test['category_hint'] = 'urine'
            
            tests.append(test)
        
        return tests
    
    def _find_column(self, df, keywords):
        """키워드로 컬럼 찾기"""
        columns = [str(col).lower() for col in df.columns]
        
        for keyword in keywords:
            keyword = keyword.lower()
            for idx, col in enumerate(columns):
                if keyword in col or col in keyword:
                    return df.columns[idx]
        
        return None
    
    def get_patient_info(self):
        """환자 정보 추출 (파일명이나 시트에서)"""
        # 기본 정보
        info = {
            'name': '환자',
            'id': '',
            'date': '',
            'age': '',
            'gender': ''
        }
        
        # 파일명에서 정보 추출 시도
        filename = Path(self.file_path).stem
        
        # 환자명 추출 (한글 이름 패턴: 2-4자)
        # 예: 김수미_검체검사결과_20260121.xlsx
        name_match = re.match(r'^([가-힣]{2,4})', filename)
        if name_match:
            info['name'] = name_match.group(1)
        
        # 날짜 패턴 (YYYY-MM-DD, YYYYMMDD 등)
        date_patterns = [
            r'(\d{4}[-_]\d{2}[-_]\d{2})',
            r'(\d{4}\d{2}\d{2})',
            r'(\d{2}[-_]\d{2}[-_]\d{2})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, filename)
            if match:
                date_str = match.group(1).replace('_', '-')
                # YYYYMMDD 형식을 YYYY-MM-DD로 변환
                if len(date_str) == 8 and '-' not in date_str:
                    date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
                info['date'] = date_str
                break
        
        # 데이터에서 날짜 컬럼 확인 (결과 날짜)
        if self.data is not None and not info['date']:
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            for col in self.data.columns:
                if re.match(date_pattern, str(col)):
                    info['date'] = str(col)
                    break
        
        return info


def parse_excel_file(file_path):
    """엑셀 파일 파싱 헬퍼 함수"""
    parser = ExcelParser(file_path)
    tests = parser.parse()
    patient_info = parser.get_patient_info()
    
    return {
        'tests': tests,
        'patient_info': patient_info
    }
