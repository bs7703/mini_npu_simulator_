test_data = "data/data.json"

class ErrCode:
    TYPE_ERROR = "{required_type}is required. current type {user_type}"
    KEY_ERROR = "{key} IS UNEXPECTED KEY."
    LEN_ERROR = "{user_len} IS NOT VALID. REQUIRED LEN IS {required_len}"
    ENUM_ERROR = "{user_data} IS NOT IN ENUM. {enum_list}"