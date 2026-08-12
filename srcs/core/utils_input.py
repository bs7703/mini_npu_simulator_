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
    while (size > 0):
        print(size)
        res_list.append(data_input(spec))
        size -= 1
    return res_list

def required_input(spec, size):
    my_dict = {"filters": {_SIZE : {"A": [], "B": []}}, "patterns": {_SIZE: {"input": [], "expected": None}}}
    my_dict["filters"][_SIZE]["A"] = list_input(spec, size)
    my_dict["filters"][_SIZE]["B"] = list_input(spec, size)
    my_dict["patterns"][_SIZE]["input"] = list_input(spec, size)
    return my_dict

def json_input(path, spec):
    try:
        data = my_io.load_json(path)
        if not(my_val.validate(data, spec)):
            return None
        return data
    except Exception as e:
        print("비정상 에러가 발생했습니다.")
        print(f"내용:{e}")
        exit()