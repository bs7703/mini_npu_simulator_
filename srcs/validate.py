import data_spec
import constants
import re
import json
import os


def get_dim(obj):
    if not isinstance(obj, list):
        return 0
    if not obj:
        return 1
    return 1 + get_dim(obj[0])

def validate_tensor_recursive(data, size) -> bool:
    if not isinstance(data, list):
        return True
    if len(data) != size:
        return False
    for x in data:
        if not validate_tensor_recursive(x, size):
            return False
    return True

def match_dynamic_key(key, schema_keys):
    """스키마의 정규표현식 키와 데이터의 키를 매칭하여 변수를 추출합니다."""
    for s_key in schema_keys:
        # 정규표현식 패턴인 경우 (예: size_(?P<n>\d+))
        if "(?P<" in s_key:
            match = re.fullmatch(s_key, key)
            if match:
                return s_key, match.groupdict()
        # 일반 문자열 매칭
        elif s_key == key:
            return s_key, {}
    return None, None

def validate(data, schema, context=None):
    """메인 검증 함수 (재귀 구조)"""
    if context is None:
        context = {}

    # 1. 스키마가 딕셔너리인 경우 (구조 검사)
    if isinstance(schema, dict):
        if not isinstance(data, dict):
            print(f"Error: Expected dict but got {type(data)}")
            return False

        for d_key, d_value in data.items():
            # 스키마에서 매칭되는 키 찾기 (정규표현식 포함)
            s_key, extracted_vars = match_dynamic_key(d_key, schema.keys())
            
            if not s_key:
                print(f"Error: Unexpected key '{d_key}'")
                return False

            # 추출된 변수(n, index 등)를 컨텍스트에 업데이트
            new_context = {**context, **extracted_vars}
            
            # 재귀적으로 하위 구조 검증
            if not validate(d_value, schema[s_key], new_context):
                return False
        return True

    # 2. 스키마가 리스트인 경우 (텐서 데이터 검사)
    elif isinstance(schema, list):
        # 스키마 리스트의 첫 번째 요소가 검증 규칙이라고 가정
        # 예: ["tensor", "size_n"]
        rule_type = schema[0]
        
        if rule_type == "tensor":
            size_var_name = schema[1] # "size_n"
            # 컨텍스트에서 실제 숫자 값을 가져옴 (예: '2')
            target_size = int(context.get(size_var_name, 0))
            
            if not validate_tensor_recursive(data, target_size):
                print(f"Error: Tensor validation failed for size {target_size}")
                return False
        return True

    return False

def run_validation(file_path):
    # 1. JSON 파일 읽기
    if not os.path.exists(file_path):
        print(f"❌ 에러: {file_path} 파일이 없습니다.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # JSON 문자열을 파이썬 딕셔너리로 변환
        
        print(f"🔍 '{file_path}' 데이터를 로드했습니다. 검증을 시작합니다...")
        
        # 2. 검증 실행 (초기 컨텍스트는 빈 딕셔너리)
        # validate(데이터, 스키마, 초기컨텍스트)
        is_valid, message = validate(data, data_spec.SCHEMA, {})
        
        if is_valid:
            print("✅ 검증 성공: 데이터 구조가 스키마와 일치합니다!")
        else:
            print(f"❌ 검증 실패: {message}")
            
    except json.JSONDecodeError as e:
        print(f"🚨 JSON 문법 오류: {e}")
    except Exception as e:
        print(f"🔥 예상치 못한 오류 발생: {e}")

# 실행부
if __name__ == "__main__":
    run_validation('data.json')