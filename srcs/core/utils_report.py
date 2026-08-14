import srcs.core.utils_cal as cal
import srcs.specs.constants as const

def print_case_report(res):
    print(f"\n[{res['name']} 분석 리포트]")
    print(f"  {'필터명':<10} | {'MAC 연산 점수':>15}")
    print("  " + "-" * 35)
    
    # 각 필터별 점수 출력
    for f_name, score in res['details'].items():
        official_name = cal.normalize_label(f_name)
        # 최고점 필터에 별표 표시
        is_winner = " ⭐ (최고점)" if f_name in res['winners'] else ""
        print(f"  - {official_name:<10}: {score:>15.8f}{is_winner}")
            
    expected_label = cal.normalize_label(res['expected']) if res['expected'] else "None"
    print(f"  >> [결과: {res['status']}]")
    print(f"  >> [내용: {res['msg']}]")
    print(f"  >> [기대값: {expected_label}]")
    print("-" * 60)

def print_final_summary(summary_list):
    total = len(summary_list)
    success = len([s for s in summary_list if s['status'] == "SUCCESS"])
    error = len([s for s in summary_list if s['status'] == "ERROR"])
    undecided = len([s for s in summary_list if s['status'] == "UNDECIDED"])

    print(f"\n{'='*20} 최종 요약 리포트 {'='*20}")
    print(f" 총 테스트: {total} | 성공: {success} | 오류: {error} | 미결정: {undecided}")

    if error + undecided > 0:
        print("\n [미통과 케이스 상세]")
        for s in summary_list:
            if s['status'] != "SUCCESS":
                print(f" - {s['name']:<15} : {s['status']} ({s['msg']})")
    print("=" * 60)

def print_perf_report(perf_data, n_iter):
    print(f"\n{'='*20} PERFORMANCE ({n_iter} iter) {'='*20}")
    print(f"{'Size (N)':<10} | {'Avg Time (ms)':<15} | {'MAC Ops':<15}")
    print("-" * 50)
    for p in perf_data:
        print(f"{p['size']:<10} | {p['avg_ms']:<15.6f} | {p['ops']:<15}")
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