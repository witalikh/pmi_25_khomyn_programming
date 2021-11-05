import json


def read_from_json(filename, result, cls=dict):
    with open(filename, mode="rt", encoding="UTF-8") as file:
        data = json.load(file)

        for element in data:
            if cls != dict:
                result.append(cls(**element))
            else:
                result.append(element)


def write_into_json(filename, iterable):
    data = []
    for element in iterable:
        data.append(dict(element))

    with open(filename, mode="wt", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, default=str)
