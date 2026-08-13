import re

#스키마키에서 해당하는키를찾고, 필요한 검색인덱스를 추출해 해당하는키와 밸류를반환
def match_dynamic_key(target_key, schema_keys):
    for s_key in schema_keys:
        if isinstance(s_key, re.Pattern):
            match = s_key.fullmatch(target_key)
            if match:
                return s_key, match.groupdict()
        elif s_key == target_key:
            return s_key, {}
    return None, {}