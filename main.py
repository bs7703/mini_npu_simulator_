import srcs.core.validate as val
import srcs.core.utils_io as utils
import srcs.specs.data_spec as spec

def main():
    data = utils.load_json("data/data.json")
    print(val.validate(data, spec.SCHEMA))
if __name__ == "__main__":
    main()