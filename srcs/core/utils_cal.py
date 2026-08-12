import json

def mac(filter_matrix: list, pattern_matrix: list, size: int, recursive=1):
    res = 0.0
    for _ in range(recursive):
        res = 0.0
        for a in range(size):
            for b in range(size):
                res += filter_matrix[a][b] * pattern_matrix[a][b]
    return res

def match_filter_pattern(filters_dict: dict, pattern_matrix: list, size: int):
    # 1. 기준 점수(base_score) 계산: 패턴의 모든 요소의 합
    
    
    res = {} # 결과를 담을 딕셔너리 초기화
    
    for filter_name, filter_data in filters_dict.items():
        # 2. MAC 연산으로 현재 필터의 점수 계산
        base_score = sum(sum(row) for row in filter_data)
        score = mac(filter_data, pattern_matrix, size)
        
        # 3. [핵심] 부동소수점 오차 비교 정책 적용
        # 차이의 절댓값이 1e-9 미만이면 matched = True
        is_matched = abs(base_score - score) < 1e-9
        
        res[filter_name] = {
            "base": base_score,
            "res": score,
            "matched": is_matched
        }
    return res

def data_result(data: dict):
    # JSON 데이터에서 패턴들을 하나씩 꺼내어 검사
    for p_name, p_info in data['patterns'].items():
        pattern_matrix = p_info['input']
        size = len(pattern_matrix)
        size_key = f"size_{size}"
        
        # 해당 사이즈의 필터 그룹이 있는지 확인
        if size_key in data['filters']:
            filters_to_test = data['filters'][size_key]
            
            # 매칭 함수 호출
            match_results = match_filter_pattern(filters_to_test, pattern_matrix, size)
            
            print(f"[{p_name}] (Expected: {p_info['expected']})")
            for f_name, result in match_results.items():
                match_status = "✅ 일치(True)" if result['matched'] else "❌ 불일치(False)"
                print(f"  - Filter '{f_name}': Score {result['res']:.10f} -> {match_status}, base_score {result['base']}")
            print("-" * 50)
