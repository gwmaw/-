"""
검사 결과 분석 및 그룹화 모듈
"""

try:
    from .test_definitions import (
        TEST_GROUPS, 
        find_test_group, 
        get_reference_range,
        is_abnormal,
        get_abnormal_direction
    )
except ImportError:
    from test_definitions import (
        TEST_GROUPS, 
        find_test_group, 
        get_reference_range,
        is_abnormal,
        get_abnormal_direction
    )


class ReportAnalyzer:
    """검사 결과를 분석하고 그룹화하는 클래스"""
    
    def __init__(self, tests, has_diabetes=False):
        self.tests = tests
        self.has_diabetes = has_diabetes
        self.grouped_tests = {}
        self.summary = {
            'total': 0,
            'normal': 0,
            'abnormal': 0,
            'abnormal_groups': []
        }
    
    def _parse_excel_reference(self, reference_str, unit=''):
        """엑셀의 참고치 문자열을 파싱하여 dict로 변환"""
        import re
        
        if not reference_str:
            return None
        
        # 패턴: "0.4 ~ 1.3", "6 ~ 20", "0 - 199", "≤ 0.30", "> 60" 등
        # 범위 형식 (min ~ max 또는 min - max)
        range_pattern = r'([\d.]+)\s*[~\-−]\s*([\d.]+)'
        match = re.search(range_pattern, reference_str)
        
        if match:
            min_val = float(match.group(1))
            max_val = float(match.group(2))
            return {
                'min': min_val,
                'max': max_val,
                'unit': unit
            }
        
        # 단일 상한값 (≤, <)
        upper_pattern = r'[≤<]\s*([\d.]+)'
        match = re.search(upper_pattern, reference_str)
        if match:
            max_val = float(match.group(1))
            return {
                'min': 0.0,
                'max': max_val,
                'unit': unit
            }
        
        # 단일 하한값 (≥, >)
        lower_pattern = r'[≥>]\s*([\d.]+)'
        match = re.search(lower_pattern, reference_str)
        if match:
            min_val = float(match.group(1))
            return {
                'min': min_val,
                'max': 999999,  # 큰 값으로 설정
                'unit': unit
            }
        
        # 문자열 값 (Negative, Positive 등)
        return {
            'value': reference_str,
            'unit': unit
        }
    
    def analyze(self):
        """검사 결과 분석 및 그룹화"""
        # 그룹 초기화
        for group_key in TEST_GROUPS.keys():
            self.grouped_tests[group_key] = {
                'info': TEST_GROUPS[group_key],
                'tests': [],
                'abnormal_count': 0
            }
        
        # 그룹화되지 않은 항목을 위한 기타 그룹
        self.grouped_tests['other'] = {
            'info': {
                'name': '기타 검사',
                'icon': '📋',
                'color': '#95A5A6'
            },
            'tests': [],
            'abnormal_count': 0
        }
        
        # 각 검사 항목 분석
        for test in self.tests:
            analyzed_test = self._analyze_test(test)
            
            # 그룹 찾기 (category_hint 우선 사용)
            group_key = None
            if 'category_hint' in test:
                group_key = test['category_hint']
            
            # category_hint가 없으면 이름으로 찾기
            if group_key is None:
                group_key = find_test_group(test['name'])
            
            if group_key is None:
                group_key = 'other'
            
            # 혈액학 검사 필터링: 빈혈수치(Hb), 백혈구수(WBC), 혈소판수(PLT)만 표시
            if group_key == 'blood':
                test_name = test['name']
                # 주요 3개 항목만 포함
                blood_main_keywords = ['빈혈수치', 'Hb', '백혈구수', 'WBC', '혈소판수', 'PLT']
                
                # 정확한 매칭 확인
                is_main_test = False
                for keyword in blood_main_keywords:
                    if keyword.lower() in test_name.lower():
                        # Hb는 HbA1c와 구분
                        if keyword.lower() == 'hb' and 'a1c' in test_name.lower():
                            continue
                        is_main_test = True
                        break
                
                # 주요 항목이 아니면 건너뜀
                if not is_main_test:
                    continue
            
            # 그룹에 추가
            self.grouped_tests[group_key]['tests'].append(analyzed_test)
            
            # 이상 소견 카운트
            if analyzed_test['is_abnormal']:
                self.grouped_tests[group_key]['abnormal_count'] += 1
        
        # 빈 그룹 제거
        self.grouped_tests = {
            k: v for k, v in self.grouped_tests.items() 
            if len(v['tests']) > 0
        }
        
        # 요약 생성
        self._generate_summary()
        
        return {
            'grouped_tests': self.grouped_tests,
            'summary': self.summary
        }
    
    def _analyze_test(self, test):
        """개별 검사 항목 분석"""
        test_name = test['name']
        result = test['result']
        
        # 참조 범위 가져오기 (우선순위: 엑셀 > test_definitions.py)
        excel_reference = test.get('reference', '').strip()
        ref_range = None
        
        # 1순위: 엑셀의 참고치 파싱
        if excel_reference:
            ref_range = self._parse_excel_reference(excel_reference, test.get('unit', ''))
        
        # 2순위: test_definitions.py의 참고치 (fallback)
        if not ref_range:
            ref_range = get_reference_range(test_name)
        
        # 당뇨 환자의 경우 HbA1c와 LDL 참고치 조정
        if self.has_diabetes and ref_range:
            # HbA1c: 7.0% 이하를 정상으로
            if 'HbA1c' in test_name or '당화혈색소' in test_name:
                ref_range = {
                    'min': ref_range.get('min', 0),
                    'max': 7.0,
                    'unit': ref_range.get('unit', '%')
                }
            # LDL: 100 mg/dL 이하를 정상으로
            elif 'LDL' in test_name or '저밀도콜레스테롤' in test_name:
                ref_range = {
                    'min': ref_range.get('min', 0),
                    'max': 100,
                    'unit': ref_range.get('unit', 'mg/dL')
                }
        
        # 이상 여부 판별 (파싱된 참고치 우선 사용)
        abnormal = False
        direction = None
        
        if ref_range and ('min' in ref_range or 'max' in ref_range):
            # 참고치가 있으면 직접 판별
            try:
                result_value = float(str(result).replace(',', '').replace('>', '').replace('<', '').replace('≤', '').replace('≥', ''))
                
                if 'max' in ref_range and result_value > ref_range['max']:
                    abnormal = True
                    direction = 'high'
                elif 'min' in ref_range and result_value < ref_range['min']:
                    abnormal = True
                    direction = 'low'
            except (ValueError, TypeError):
                # 숫자가 아닌 경우 기본 로직 사용
                abnormal = is_abnormal(test_name, result)
                direction = get_abnormal_direction(test_name, result) if abnormal else None
        else:
            # 참고치가 없으면 기본 로직 사용
            abnormal = is_abnormal(test_name, result)
            direction = get_abnormal_direction(test_name, result) if abnormal else None
        
        # 단위 설정
        unit = test.get('unit', '')
        if not unit and ref_range:
            unit = ref_range.get('unit', '')
        
        # 참조 범위 문자열 생성
        # 우선순위: 엑셀 파일의 참조 범위 > 우리가 정의한 참조 범위
        reference_str = ''
        
        # 1순위: 엑셀의 참고치 사용
        excel_reference = test.get('reference', '').strip()
        if excel_reference:
            reference_str = excel_reference
        
        # 2순위: test_definitions.py의 참고치 사용 (fallback)
        if not reference_str and ref_range:
            if 'min' in ref_range and 'max' in ref_range:
                reference_str = f"{ref_range['min']} - {ref_range['max']}"
            elif 'value' in ref_range:
                reference_str = ref_range['value']
        
        return {
            'name': test_name,
            'result': result,
            'unit': unit,
            'reference': reference_str,
            'is_abnormal': abnormal,
            'direction': direction,
            'ref_range': ref_range
        }
    
    def _generate_summary(self):
        """검사 결과 요약 생성"""
        total = 0
        abnormal = 0
        abnormal_groups = []
        
        for group_key, group_data in self.grouped_tests.items():
            group_total = len(group_data['tests'])
            group_abnormal = group_data['abnormal_count']
            
            total += group_total
            abnormal += group_abnormal
            
            # 이상 소견이 있는 그룹 저장
            if group_abnormal > 0:
                abnormal_groups.append({
                    'name': group_data['info']['name'],
                    'icon': group_data['info']['icon'],
                    'count': group_abnormal
                })
        
        self.summary = {
            'total': total,
            'normal': total - abnormal,
            'abnormal': abnormal,
            'abnormal_groups': abnormal_groups
        }
    
    def get_abnormal_tests(self):
        """이상 소견 항목만 추출"""
        abnormal_tests = []
        
        for group_key, group_data in self.grouped_tests.items():
            for test in group_data['tests']:
                if test['is_abnormal']:
                    abnormal_tests.append({
                        'group': group_data['info']['name'],
                        'test': test
                    })
        
        return abnormal_tests
    
    def get_recommendations(self):
        """이상 소견에 대한 권장사항 생성"""
        recommendations = []
        abnormal_tests = self.get_abnormal_tests()
        
        # 그룹별 권장사항
        group_recommendations = {
            'liver': '간기능 이상이 관찰되었습니다. 음주를 자제하고 규칙적인 운동과 균형잡힌 식사를 권장합니다.',
            'kidney': '신기능 이상이 관찰되었습니다. 충분한 수분 섭취와 저염식을 권장합니다.',
            'diabetes': '혈당 조절이 필요합니다. 규칙적인 식사와 운동, 체중 관리를 권장합니다.',
            'lipid': '지질 관리가 필요합니다. 저지방 식단과 규칙적인 운동을 권장합니다.',
            'blood': '혈액학적 이상이 관찰되었습니다. 추가 검사가 필요할 수 있습니다.',
            'thyroid': '갑상선 기능 이상이 관찰되었습니다. 전문의 상담을 권장합니다.',
            'urine': '소변 검사 이상이 관찰되었습니다. 추가 검사가 필요할 수 있습니다.'
        }
        
        # 이상 소견이 있는 그룹의 권장사항 추가
        added_groups = set()
        for item in abnormal_tests:
            group_key = find_test_group(item['test']['name'])
            if group_key and group_key not in added_groups:
                if group_key in group_recommendations:
                    recommendations.append(group_recommendations[group_key])
                    added_groups.add(group_key)
        
        # 이상 소견이 없으면 일반 권장사항
        if not recommendations:
            recommendations.append('모든 검사 결과가 정상 범위 내에 있습니다. 건강한 생활습관을 유지하시기 바랍니다.')
        
        return recommendations


def analyze_test_results(tests, has_diabetes=False):
    """검사 결과 분석 헬퍼 함수
    
    Args:
        tests: 검사 결과 리스트
        has_diabetes: 당뇨병 환자 여부 (True일 경우 HbA1c, LDL 기준 조정)
    """
    analyzer = ReportAnalyzer(tests, has_diabetes=has_diabetes)
    analysis = analyzer.analyze()
    
    return {
        'grouped_tests': analysis['grouped_tests'],
        'summary': analysis['summary'],
        'abnormal_tests': analyzer.get_abnormal_tests(),
        'recommendations': analyzer.get_recommendations()
    }
