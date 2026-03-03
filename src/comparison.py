"""
검사 결과 비교 모듈
최신 검사와 이전 검사 결과를 비교하여 변화 추이 분석
"""

def compare_test_results(current_tests, previous_tests):
    """
    최신 검사와 이전 검사 결과 비교
    
    Args:
        current_tests: 최신 검사 결과 리스트
        previous_tests: 이전 검사 결과 리스트
    
    Returns:
        comparison_data: 비교 결과 딕셔너리
    """
    comparison = {}
    
    # 이전 검사 결과를 검사명으로 매핑
    prev_test_map = {normalize_test_name(test['name']): test for test in previous_tests}
    
    for current_test in current_tests:
        test_name = current_test['name']
        normalized_name = normalize_test_name(test_name)
        
        comparison[test_name] = {
            'current': current_test,
            'previous': None,
            'change': None,
            'change_percent': None,
            'trend': None,  # 'improved', 'worsened', 'stable', 'new'
            'has_comparison': False
        }
        
        # 이전 검사에서 동일한 항목 찾기
        if normalized_name in prev_test_map:
            prev_test = prev_test_map[normalized_name]
            comparison[test_name]['previous'] = prev_test
            comparison[test_name]['has_comparison'] = True
            
            # 수치 변화 계산
            current_value = extract_numeric_value(current_test['result'])
            prev_value = extract_numeric_value(prev_test['result'])
            
            if current_value is not None and prev_value is not None:
                change = current_value - prev_value
                change_percent = ((current_value - prev_value) / prev_value * 100) if prev_value != 0 else 0
                
                comparison[test_name]['change'] = change
                comparison[test_name]['change_percent'] = change_percent
                
                # 추세 분석
                trend = analyze_trend(
                    current_test=current_test,
                    previous_test=prev_test,
                    change=change,
                    change_percent=change_percent
                )
                comparison[test_name]['trend'] = trend
        else:
            comparison[test_name]['trend'] = 'new'
    
    return comparison


def normalize_test_name(test_name):
    """
    검사명 정규화 (비교를 위해)
    예: "신장기능(Cr)" -> "creatinine"
    """
    # 괄호 안의 내용 추출
    import re
    
    # 괄호 제거 및 공백 제거
    normalized = test_name.replace('(', ' ').replace(')', ' ').replace('-', ' ').strip().lower()
    
    # 여러 공백을 하나로
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized


def extract_numeric_value(result_str):
    """
    결과 문자열에서 숫자 값 추출
    예: "1.29 mg/dl" -> 1.29
    """
    import re
    
    if not result_str or result_str in ['-', 'Negative', '음성']:
        return None
    
    # 화살표 제거
    result_str = result_str.replace('↑', '').replace('↓', '').replace('▲', '').replace('▼', '').strip()
    
    # 숫자 추출 (소수점 포함)
    match = re.search(r'[-+]?\d+\.?\d*', str(result_str))
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    
    return None


def analyze_trend(current_test, previous_test, change, change_percent):
    """
    검사 결과 추세 분석
    
    Returns:
        'improved': 개선됨 (정상 범위로 가까워짐)
        'worsened': 악화됨 (비정상 범위로 멀어짐)
        'stable': 안정적 (변화 미미)
        'changed': 변화 있음 (판단 불가)
    """
    # 변화량이 매우 작으면 stable
    if abs(change_percent) < 5:
        return 'stable'
    
    # 현재 상태 확인
    current_abnormal = current_test.get('abnormal', False)
    prev_abnormal = previous_test.get('abnormal', False)
    
    # 비정상 -> 정상
    if prev_abnormal and not current_abnormal:
        return 'improved'
    
    # 정상 -> 비정상
    if not prev_abnormal and current_abnormal:
        return 'worsened'
    
    # 둘 다 정상 또는 둘 다 비정상인 경우
    if current_abnormal:
        # 비정상인데 참고치 중심에 가까워졌는지 확인
        current_ref = current_test.get('reference_range')
        if current_ref and 'min' in current_ref and 'max' in current_ref:
            ref_min = current_ref['min']
            ref_max = current_ref['max']
            ref_mid = (ref_min + ref_max) / 2
            
            current_value = extract_numeric_value(current_test['result'])
            prev_value = extract_numeric_value(previous_test['result'])
            
            if current_value and prev_value and ref_mid:
                # 참고치 중심으로부터의 거리
                current_distance = abs(current_value - ref_mid)
                prev_distance = abs(prev_value - ref_mid)
                
                if current_distance < prev_distance:
                    return 'improved'
                elif current_distance > prev_distance:
                    return 'worsened'
    
    # 변화는 있지만 개선/악화 판단 불가
    return 'changed'


def generate_comparison_summary(comparison_data):
    """
    비교 결과 요약 생성
    
    Returns:
        summary: 비교 결과 요약 딕셔너리
    """
    total_compared = sum(1 for v in comparison_data.values() if v['has_comparison'])
    total_new = sum(1 for v in comparison_data.values() if v['trend'] == 'new')
    
    improved_count = sum(1 for v in comparison_data.values() if v['trend'] == 'improved')
    worsened_count = sum(1 for v in comparison_data.values() if v['trend'] == 'worsened')
    stable_count = sum(1 for v in comparison_data.values() if v['trend'] == 'stable')
    
    # 주요 변화 항목 (변화율 상위 5개)
    significant_changes = []
    for test_name, data in comparison_data.items():
        if data['has_comparison'] and data['change_percent'] is not None:
            significant_changes.append({
                'name': test_name,
                'change_percent': data['change_percent'],
                'trend': data['trend']
            })
    
    # 절대값 기준 정렬
    significant_changes.sort(key=lambda x: abs(x['change_percent']), reverse=True)
    significant_changes = significant_changes[:5]
    
    return {
        'total_compared': total_compared,
        'total_new': total_new,
        'improved_count': improved_count,
        'worsened_count': worsened_count,
        'stable_count': stable_count,
        'significant_changes': significant_changes
    }


def format_change(change, unit=''):
    """
    변화량 포맷팅
    예: +1.5 mg/dl, -3.2%
    """
    if change is None:
        return ''
    
    sign = '+' if change > 0 else ''
    return f"{sign}{change:.2f} {unit}".strip()


def format_trend_icon(trend):
    """
    추세 아이콘 반환
    """
    icons = {
        'improved': '✅',
        'worsened': '⚠️',
        'stable': '➡️',
        'changed': '🔄',
        'new': '🆕'
    }
    return icons.get(trend, '')


def format_trend_text(trend):
    """
    추세 텍스트 반환
    """
    texts = {
        'improved': '개선',
        'worsened': '악화',
        'stable': '유지',
        'changed': '변화',
        'new': '신규'
    }
    return texts.get(trend, '')
