import srcs.core.utils_input as my_input
import srcs.core.utils_report as my_report
import srcs.specs.data_spec as my_spec

EXIT_MENU = 3
USER_INPUT_ARRAY_SIZE = 3
PATH = "data/data.json" 

prompt_spec = [
    {"menu": "handle_input", "func": my_input.required_input, "params": {"spec": [my_input.to_float_list], "size": USER_INPUT_ARRAY_SIZE}},
    {"menu": "jason_load and validate", "func": my_input.json_input, "params": {"path":PATH, "spec":my_spec.SCHEMA}},
    {"menu": "exit", "func": exit, "params": {}}
]

def run(prompt: list = prompt_spec):
    while True:
        try:
            print("\n--- 프롬프트 메뉴를 선택해주세요 ---")
            for i, item in enumerate(prompt):
                print(f"{i}. {item['menu']}")
                
            # 사용자 입력 받기
            user_choice = my_input.data_input([int])
            
            # 종료 조건 처리
            if user_choice == len(prompt):
                print("프로그램을 종료합니다.")
                break

            # 메뉴 선택 및 실행
            selected_menu = prompt[user_choice]
            print(f">>> 선택된 메뉴: {selected_menu['menu']}")

            # 함수 실행 (가독성을 위해 params가 없을 경우 대비)
            func = selected_menu["func"]
            params = selected_menu.get("params", {}) # params가 없을 경우 빈 딕셔너리
            
            data = func(**params)

            if data is not None:
                my_report.data_result(data)
            else:
                print("결과 데이터가 없습니다.")
            
        except IndexError:
            print(f"잘못된 번호입니다. 0부터 {len(prompt)} 사이의 숫자를 입력하세요.")
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    run(prompt_spec)