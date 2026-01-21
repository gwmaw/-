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
        unit_cols = self._find_column(df, ['단위', 'unit', 'units'])
        ref_cols = self._find_column(df, ['정상범위', '참고치', 'reference', 'ref', 'range', 'normal'])
        
        # 결과 컬럼이 없으면 날짜 컬럼을 찾기 (YYYY-MM-DD 형식)
        if result_cols is None:
            # 날짜 형식 컬럼 찾기
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
        for idx, row in df.iterrows():
            test_name = str(row[test_name_cols]).strip()
            result_value = row[result_cols]
            
            # 빈 행이나 헤더 행 건너뛰기
            if pd.isna(test_name) or test_name == '' or test_name.lower() in ['nan', 'none']:
                continue
            
            # 결과값 정리
            if pd.isna(result_value):
                result_value = ''
            else:
                result_value = str(result_value).strip()
            
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
            
            # 검사 데이터 저장
            test = {
                'name': test_name,
                'result': result_clean if result_clean else result_value,
                'unit': unit,
                'reference': reference,
                'original_result': original_result  # 원본 결과 저장
            }
            
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
