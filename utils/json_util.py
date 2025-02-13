import json


def save_json(save_path, the_dict):
    with open(save_path, "w") as f:
        content = json.dumps(the_dict,ensure_ascii=False)
        f.write(content)


def load_json(save_path):
    with open(save_path, "r") as f:
        the_dict = json.load(f)
        return the_dict
