# srcs/specs/constants.py
TEST_DATA = "data/data.json"

# 필터 키와 출력 기호 매핑
NAME_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X",
}

class ErrCode:
    TYPE_ERROR = "{required_type} is required. current type {user_type}"
    KEY_ERROR = "{key} IS UNEXPECTED KEY."
    LEN_ERROR = "{user_len} IS NOT VALID. REQUIRED LEN IS {required_len}"
    ENUM_ERROR = "{user_data} IS NOT IN ENUM. {enum_list}"