import _pickle as pickle  # python3
import time
import json


def read_pickle(filepath):
    f = open(filepath, 'rb')
    word2mfccs = pickle.load(f)
    f.close()
    return word2mfccs


def save_pickle(save_path, save_data):
    f = open(save_path, 'wb')
    pickle.dump(save_data, f)
    f.close()


def read_json(filepath):
    with open(filepath) as f:
        obj = json.load(f)
    return obj


def save_json(save_path, obj):
    with open(save_path, 'w') as f:
        json.dump(obj, f)


def save_json_lines(save_path, lines):
    assert type(lines) == list
    with open(save_path, 'w') as f:
        for obj in lines:
            f.write(json.dumps(obj) + "\n")


def read_json_lines(filepath):
    data = []
    with open(filepath) as f:
        for line in f:
            obj = json.loads(line)
            data.append(obj)
    return data
