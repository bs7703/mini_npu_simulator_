import srcs.specs.constants as const

def validate_tensor(data, spec, context):
    size = int(context.get("N", 0))
    target_type = spec.get("data_type", float)
    if not isinstance(data, list):
        if isinstance(data, target_type):
            return True, ""
        return False, const.ErrCode.TYPE_ERROR.format(required_type = str(type(target_type)), user_type = str(type(data)))
    if len(data) != size:
        return False, const.ErrCode.LEN_ERROR.format(user_len = len(data), required_len = size)
    for x in data:
        res, msg = validate_tensor(x, spec, context)
        if not res:
            return False, msg
    return True, ""

def validate_list(data, spec, context) :
    if data in spec.get("enum", []):
        return True, ""
    return False, const.ErrCode.ENUM_ERROR.format(user_data = str(type(data)), enum_list = spec.get("enum"))

RULE_MAPS = {"TENSOR_RULE": validate_tensor, "LIST_RULE": validate_list}