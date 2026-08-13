import srcs.core.validate as my_val
import srcs.core.utils_io as my_io

INPUT_SIZE = 3
_SIZE = f"size_{INPUT_SIZE}"

def to_float_list(str):
    return  [float(x) for x in str.split()]

def data_input(spec):
    while True:
        is_valid = True
        try:
            value = spec[0](input().strip())
            for a in spec[1:]:
                if not (a(value)):
                    print("적절한 값 범위가 아닙니다. 재입력하세요")
                    is_valid = False
        except EOFError:
            raise EOFError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except ValueError:
            print("적절한 값이 입력되지 않았습니다.")
            is_valid = False
        if (is_valid):
            return value

def list_input(spec, size):
    res_list = []
    total = size
    while (size > 0):
        # 몇 번째 줄을 입력 중인지 표시
        print(f"  > {total - size + 1}행 입력 대기 중...", end=" ")
        res_list.append(data_input(spec))
        size -= 1
    return res_list

def required_input(spec, size):
    size_key = f"size_{size}"
    print(f"\n{'='*20} 수동 데이터 입력 모드 ({size}x{size}) {'='*20}")
    print(f"\n[1/3] 필터 A (Cross) 설정을 시작합니다.")
    filter_A= list_input(spec, size)
    print(f"\n[2/3] 필터 B (X) 설정을 시작합니다.")
    filter_B = list_input(spec, size)
    print(f"\n{'*'*10} 필터 설정이 완료되었습니다. {'*'*10}")
    print(f"\n[3/3] 분석할 테스트 패턴을 입력하세요.")
    pattern_input = list_input(spec, size)
    my_dict = {
        "filters": {
            size_key: {
                "A": filter_A,
                "B": filter_B
            }
        },
        "patterns": {
            "size_3": {
                "input": pattern_input,
                "expected": None # 수동 입력의 기본 기대값 설정
            }
        }
    }
    
    print(f"\n{'='*20} 모든 입력이 완료되었습니다! {'='*20}\n")
    return my_dict

def json_input(path, spec):
    try:
        data = my_io.load_json(path)
        if not(my_val.validate(data, spec)):
            return None
        print("데이터 무결성 검증이 완료되고, 필터가 전부 로드되었습니다.")
        return data
    except Exception as e:
        print("비정상 에러가 발생했습니다.")
        print(f"내용:{e}")
        exit()