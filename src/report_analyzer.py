"""
검사 결과 분석 및 그룹화 모듈
"""

from .test_definitions import (
    TEST_GROUPS, 
    find_test_group, 
    get_reference_range,
    is_abnormal,
    get_abnormal_direction
)


class ReportAnalyzer:
    """검사 결과를 분석하고 그룹화하는 클래스"""
    
    def __init__(self, tests):
        self.tests = tests
        self.grouped_tests = {}
        self.summary = {
            'total': 0,
            'normal': 0,
            'abnormal': 0,
            'abnormal_groups': []
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
        
        # 참조 범위 가져오기
        ref_range = get_reference_range(test_name)
        
        # 이상 여부 판별
        abnormal = is_abnormal(test_name, result)
        
        # 이상 방향 (높음/낮음)
        direction = get_abnormal_direction(test_name, result) if abnormal else None
        
        # 단위 설정
        unit = test.get('unit', '')
        if not unit and ref_range:
            unit = ref_range.get('unit', '')
        
        # 참조 범위 문자열 생성
        # 우선순위: 우리가 정의한 간소화된 참조 범위 > 엑셀 파일의 참조 범위
        reference_str = ''
        if ref_range:
            if 'min' in ref_range and 'max' in ref_range:
                reference_str = f"{ref_range['min']} - {ref_range['max']}"
            elif 'value' in ref_range:
                reference_str = ref_range['value']
        
        # 참조 범위가 없으면 엑셀 파일의 값 사용
        if not reference_str:
            reference_str = test.get('reference', '')
        
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


def analyze_test_results(tests):
    """검사 결과 분석 헬퍼 함수"""
    analyzer = ReportAnalyzer(tests)
    analysis = analyzer.analyze()
    
    return {
        'grouped_tests': analysis['grouped_tests'],
        'summary': analysis['summary'],
        'abnormal_tests': analyzer.get_abnormal_tests(),
        'recommendations': analyzer.get_recommendations()
    }
