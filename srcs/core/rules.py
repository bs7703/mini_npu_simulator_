import srcs.specs.constants as const

def validate_tensor(data, spec, context) -> tuple[bool, str]:
    size = int(context.get("N", 0))
    target_type = spec.get("data_type", int)
    if not isinstance(data, list):
        if isinstance(data, target_type):
            return True, ""
        return False, const.ErrCode.TYPE_ERROR.format(...)
    if len(data) != size:
        return False, const.ErrCode.LEN_ERROR.format(...)
    for x in data:
        res, msg = validate_tensor(x, spec, context)
        if not res:
            return False, msg
    return True, ""

def validate_list(data, spec, context) -> tuple[bool, str]:
    if data in spec.get("enum", []):
        return True, ""
    return False, const.ErrCode.ENUM_ERROR.format(...)

# ★ 함수 정의 후 매핑!
RULE_MAPS = {"TENSOR_RULE": validate_tensor, "LIST_RULE": validate_list}