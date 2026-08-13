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

def match_filter_pattern(filters_dict, pattern_matrix, size):
    res = {}
    for f_name, f_data in filters_dict.items():
        base_score = sum(sum(row) for row in f_data)
        score = mac(f_data, pattern_matrix, size)
        is_matched = abs(base_score - score) < 1e-9
        res[f_name] = {"base": base_score, "res": score, "matched": is_matched}
    return res

def analyze_test_case(p_name, p_info, filters_data):
    pattern_matrix = p_info['input']
    expected = p_info['expected']
    size = len(pattern_matrix)
    size_key = f"size_{size}"
    result = {"name": p_name, "is_pass": False, "expected": expected, "actual": [], "reason": "", "details": {}}

    if size_key not in filters_data:
        result["reason"] = f"Missing filters for {size_key}"
        return result

    match_res = match_filter_pattern(filters_data[size_key], pattern_matrix, size)
    result["details"] = match_res
    
    matched_keys = [k for k, v in match_res.items() if v['matched']]
    actual_symbols = [const.NAME_MAP.get(k, k) for k in matched_keys]
    result["actual"] = actual_symbols
    expected = const.NAME_MAP.get(expected, expected)

    if not matched_keys:
        result["reason"] = "result:No filter matched (Score Mismatch)."
    elif len(matched_keys) > 1:
        result["reason"] = "result:undecided"
    else:
        if (actual_symbols[0] == expected) or expected is None:
            result["is_pass"] = True
        else:
            result["reason"] = f"Classification error (Got {actual_symbols[0]}, Expected {expected})"
    return result

def get_performance_data(data, n_iterations = 10):
    perf_results = []
    size_keys = sorted([int(k.split('_')[1]) for k in data.get('filters', {}).keys() if k.startswith("size_")])
    for n in size_keys:
        dummy = [[0.5]*n for _ in range(n)]
        start = time.perf_counter()
        mac(dummy, dummy, n, n_iterations)
        avg_time = ((time.perf_counter() - start) / n_iterations) * 1000
        perf_results.append({"size": n, "avg_ms": avg_time, "ops": n*n})
    return perf_results