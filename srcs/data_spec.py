TENSOR_RULE = "validate_tensor"
ALLOWED_OPS = ["+", "x"]

#따로 매핑없이 리스트면 내부항목일치검사, 특정 딕셔너리면 매핑함수 제작후 검사함수 매핑
#만약 구조별 세분화 원자함수 배치가필요했다면, 최하단에서 재매핑하는 구조로설계

SCHEMA = {
    "filters": {          
        "cross": {       
            r"size_(?P<N>\d+)_(?P<idx>\d+)":
            {
                "cross" : TENSOR_RULE,
                "x" : TENSOR_RULE
            }
        }
    },
    "patterns": {
        "input": {
            r"size_(?P<N>\d+)": TENSOR_RULE
        },
        "expected" : ALLOWED_OPS
    }
}