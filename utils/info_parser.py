from utils import pickle_util
import os
import json


def parse_info(folder_path):
    # 判断有没有info.json
    if os.path.exists(os.path.join(folder_path, "info.json")):
        info, detail_dict = parse_info_json(folder_path)
    elif os.path.exists(os.path.join(folder_path, "junper-tongtong-sim.pkl")):
        info, detail_dict = parse_pkl(folder_path, "junper-tongtong-sim.pkl")
    else:
        info, detail_dict = None, None
    return info, detail_dict


def parse_info_json(folder_path):
    try:
        with open(os.path.join(folder_path, "info.json"), 'r') as f:
            info = json.load(f)
            detail_dict = info['detail']
            del info['detail']
        return info, detail_dict
    except Exception as e:
        return None, None


def parse_pkl(rootpath, pkl_name):
    try:
        pkl_path = os.path.join(rootpath, pkl_name)
        info = pickle_util.read_pickle(pkl_path)
        results = info['results']
        del info['results']

        detail_dict = {}
        for obj in results:
            name = obj['file'].split("/")[-1]
            del obj['file']
            detail_dict[name] = obj

        return info, detail_dict
    except Exception as e:
        return None, None
