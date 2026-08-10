import json

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except PermissionError:
        raise PermissionError
    except FileNotFoundError:
        raise FileNotFoundError
    except json.JSONDecodeError:
        raise ValueError(f"JSON 형식이 올바르지 않습니다.: {path}")
    except Exception as e:
        raise RuntimeError(f"파일 로드중 예상치 못한 오류 발생: {e}")

def save_json(path, data):
    try:
        with open(path, "w", encoding= "utf-8"):
            return json.dump(data)
    except FileNotFoundError:
        raise FileNotFoundError
    except TypeError as e:
        raise ValueError(f"JSON으로 변환할수 없는 데이터가 있습니다.")
    except PermissionError:
        raise PermissionError
    except Exception as e:
        raise RuntimeError(f"파일 세이브중 예상치 못한 오류 발생: {e}")
