import srcs.core.utils_cal as cal
import srcs.specs.constants as const

def print_case_report(res):
    print(f"\n[{res['name']}]")
    print(f"  {'FILTER':<10} | {'MAC_SCORE':>12} | {'FILTER_SCORE':>12}")
    print("  " + "-" * 45)
    
    matched_filters = []
    for f_name, d in res['details'].items():
        official_name = cal.normalize_label(f_name)
        status_icon = '✅' if d['matched'] else '❌'
        print(f"  - {official_name:<10}: {d['res']:.8f}, {d['base']:.8f} {status_icon}")
        if d['matched']:
            matched_filters.append(official_name)
            
    match_count = len(matched_filters)
    
    if match_count == 1:
        res['status'] = "SUCCESS"
        res['msg'] = f"Identified as '{matched_filters[0]}'"
    elif match_count > 1:
        res['status'] = "UNDECIDED"
        res['msg'] = f"Tie detected: {', '.join(matched_filters)}"
    else:
        res['status'] = "FAIL"
        res['msg'] = "No pattern matched threshold"
    print(f"  >> [{res['status']}]: {res['msg']}, expected-> {cal.normalize_label(res['expected'])}")
    print("-" * 60)

def print_perf_report(perf_data, n_iter):
    print(f"\n{'='*20} PERFORMANCE ({n_iter} iter) {'='*20}")
    print(f"{'Size (N)':<10} | {'Avg Time (ms)':<15} | {'MAC Ops':<15}")
    print("-" * 50)
    for p in perf_data:
        print(f"{p['size']:<10} | {p['avg_ms']:<15.6f} | {p['ops']:<15}")
    print("=" * 55)

def print_final_summary(summary_list):
    total = len(summary_list)
    passed_cases = [s for s in summary_list if s['status'] == "SUCCESS"]
    failed_cases = [s for s in summary_list if s['status'] != "SUCCESS"]
    
    passed = len(passed_cases)
    failed = len(failed_cases)

    print(f"\n{'='*20} FINAL SUMMARY {'='*20}")
    print(f" Total: {total} | Pass: {passed} | Fail: {failed}")

    if failed > 0:
        print("\n [FAILED/UNDECIDED CASES]")
        for f in failed_cases:
            print(f" - {f['name']:<15} : {f['status']} ({f['msg']})")
            
    print("=" * 55)

def data_result(data, perf_n=10):
    print(f"\n{'#'*20} NPU REPORT START {'#'*20}")
    summary = []
    for p_name, p_info in data['patterns'].items():
        res = cal.analyze_test_case(p_name, p_info, data.get('filters', {}))
        print_case_report(res) 
        summary.append(res)
        
    perf_data = cal.get_performance_data(data, perf_n)
    print_perf_report(perf_data, perf_n)
    print_final_summary(summary)