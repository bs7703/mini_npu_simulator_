# srcs/specs/constants.py
TEST_DATA = "data/data.json"

# 필터 키와 출력 기호 매핑
NAME_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X",
    "A": "Cross",  # 수동 입력 필터 A 매핑
    "B": "X"   # 수동 입력 필터 B 매핑
}

class ErrCode:
    TYPE_ERROR = "{required_type} is required. current type {user_type}"
    KEY_ERROR = "{key} IS UNEXPECTED KEY."
    LEN_ERROR = "{user_len} IS NOT VALID. REQUIRED LEN IS {required_len}"
    ENUM_ERROR = "{user_data} IS NOT IN ENUM. {enum_list}"