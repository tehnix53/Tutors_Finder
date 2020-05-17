import json


def dict_to_json(sample, name):
    contents = json.dumps(sample)
    with open(name, "w") as f:
        f.write(contents)


def unpack_json(filename):
    with open(filename, "r") as f:
        contents = f.read()
    my_list = json.loads(contents)
    return my_list


def database_initialize(some_list):
    contents = json.dumps(some_list)
    with open("booking.json", "w", ) as f:
        f.write(contents)
    with open("request.json", "w", ) as f:
        f.write(contents)


def update_json(this_data, json_file):
    with open(json_file, "r", ) as f:
        contents = f.read()
    new_list = json.loads(contents)
    new_list.append([this_data])
    contents = json.dumps(new_list, ensure_ascii=False)
    with open(json_file, "w", ) as f:
        f.write(contents)
