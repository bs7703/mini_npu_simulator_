import srcs.specs.data_spec as data_spec
import srcs.specs.constants as const
import srcs.core.rules as rules
from srcs.core.regex_utils import *


def validate(data, schema, context=None):
    if context is None:
        context = {}

    if isinstance(schema, dict):
        if not isinstance(data, dict):
            print(const.ErrCode.TYPE_ERROR.format(required_type = dict, user_type = type(data)))
            return False

        for d_key, d_value in data.items():
            s_key, extracted_vars = match_dynamic_key(d_key, schema.keys())
            if not s_key:
                print(const.ErrCode.KEY_ERROR.format(key = d_key))
                return False
            new_context = {**context, **extracted_vars}
            if not validate(d_value, schema[s_key], new_context):
                return False
        return True
    elif isinstance(schema, list):
        for a in schema:
            res, msg = rules.RULE_MAPS[a["type"]](data, a, context)
            if not res:
                print(msg)
                return False
        return True