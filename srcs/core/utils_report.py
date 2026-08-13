# srcs/core/utils_report.py
import srcs.core.utils_cal as cal
import srcs.specs.constants as const

def print_case_report(res):
    print(f"[{res['name']}] (Expected: {const.NAME_MAP.get(res['expected'], res['expected'])})")
    for f_name, d in res['details'].items():
        print(f"  - {f_name:<10}: {d['res']:.4f} {'✅' if d['matched'] else '❌'}")
    if not res["is_pass"]: print(f"  >> ⚠️ [FAIL]: {res['reason']}")
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
    passed = len([s for s in summary_list if s['is_pass']])
    print(f"\n{'='*20} FINAL SUMMARY {'='*20}")
    print(f" Total: {total} | Pass: {passed} | Fail: {total-passed}")
    if total > passed:
        print("\n [FAILED CASES]")
        for f in [s for s in summary_list if not s['is_pass']]:
            print(f" - {f['name']}: {f['reason']} (Got {f['actual']})")
    print("=" * 55)

def data_result(data, perf_n=1000):
    """메인 리포트 호출 함수"""
    print(f"\n{'#'*20} NPU REPORT START {'#'*20}")
    summary = []
    for p_name, p_info in data['patterns'].items():
        res = cal.analyze_test_case(p_name, p_info, data.get('filters', {}))
        summary.append(res)
        print_case_report(res)
    perf_data = cal.get_performance_data(data, perf_n)
    print_perf_report(perf_data, perf_n)
    print_final_summary(summary)