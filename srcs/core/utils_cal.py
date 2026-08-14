# srcs/core/utils_cal.py
import time
import srcs.specs.constants as const

def normalize_label(label):
    return const.NAME_MAP.get(label, label)

def mac(filter_matrix, pattern_matrix, size, recursive=1):
    res = 0.0
    for _ in range(recursive):
        res = 0.0
        for a in range(size):
            for b in range(size):
                res += filter_matrix[a][b] * pattern_matrix[a][b]
    return res

# srcs/core/utils_cal.py

def match_filter_pattern(filters_dict, pattern_matrix, size):
    scores = {}
    for f_name, f_data in filters_dict.items():
        # 데이터 스키마 대응 (리스트 중첩 해제)
        actual_filter = f_data[0] if isinstance(f_data[0][0], list) else f_data
        # 순수 MAC 연산 점수만 계산
        scores[f_name] = mac(actual_filter, pattern_matrix, size)
    
    # 1. 최고 점수 추출
    max_val = max(scores.values())
    
    # 2. 최고 점수와 동일한(오차 1e-9 내) 필터들 추출 (동점 판별)
    winners = [name for name, val in scores.items() if abs(val - max_val) < 1e-9]
    
    return {
        "scores": scores,
        "winners": winners,
        "max_score": max_val
    }

def analyze_test_case(p_name, p_info, filters_data):
    # 입력 데이터 정규화
    pattern_matrix = p_info['input'][0] if isinstance(p_info['input'][0][0], list) else p_info['input']
    expected = p_info.get('expected')
    size = len(pattern_matrix)
    size_key = f"size_{size}"
    
    result = {
        "name": p_name, 
        "status": "ERROR", 
        "expected": expected, 
        "winners": [], 
        "msg": "", 
        "details": {}
    }

    if size_key not in filters_data:
        result["msg"] = f"Missing filters for {size_key}"
        return result

    # 최고점 판별 실행
    match_res = match_filter_pattern(filters_data[size_key], pattern_matrix, size)
    result["details"] = match_res["scores"]
    result["winners"] = match_res["winners"]
    
    winners_norm = [normalize_label(w) for w in match_res["winners"]]
    expected_norm = normalize_label(expected) if expected else None

    # --- 판정 로직 ---
    if len(winners_norm) > 1:
        # 최고점이 여러 개인 경우
        result["status"] = "UNDECIDED"
        result["msg"] = f"동점 발생(판정 불가): {', '.join(winners_norm)}"
    else:
        # 단독 최고점인 경우
        actual = winners_norm[0]
        if expected_norm is None or actual == expected_norm:
            result["status"] = "SUCCESS"
            result["msg"] = f"식별 성공: {actual}"
        else:
            result["status"] = "ERROR"
            result["msg"] = f"분류 오류 (결과: {actual}, 기대: {expected_norm})"
            
    return result

def get_performance_data(data, n_iterations = 10):
    perf_results = []
    size_keys = sorted([int(k.split('_')[1]) for k in data.get('filters', {}).keys() if k.startswith("size_")])
    matched = False
    for a in size_keys:
        if (a == 3):
            matched = True
    if not(matched):
        size_keys.insert(0, 3)
    for n in size_keys:
        dummy = [[0.5]*n for _ in range(n)]
        start = time.perf_counter()
        mac(dummy, dummy, n, n_iterations)
        avg_time = ((time.perf_counter() - start) / n_iterations) * 1000
        perf_results.append({"size": n, "avg_ms": avg_time, "ops": n*n})
    return perf_results