import glob

import flask_cors
from flask import Flask, send_from_directory, abort, send_file
from flask import Flask, jsonify, request
import json
from utils.db_util import Folder, Collection, FolderCollection
from utils import db_util
from playhouse.shortcuts import model_to_dict, dict_to_model
import os
from utils import sort_util, json_util
from utils import info_parser

db_util.do_connect()

app = Flask(__name__)
cors = flask_cors.CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

root_folder = "./frontend/dist"


@app.route('/')
def index():
    # 确保index.html存在
    index_path = os.path.join(root_folder, 'index.html')
    assert os.path.exists(index_path)
    # 返回index.html
    return send_from_directory(root_folder, 'index.html')


@app.route('/<path:filename>')
def get_file(filename):
    the_path = os.path.join(root_folder, filename)

    # 检查文件是否存在
    if not os.path.exists(the_path):
        abort(404)  # 如果文件不存在，返回404错误

        # 检查请求的文件是否为目录，如果是，则重定向到该目录下的index.html
    if os.path.isdir(the_path):
        index_path = os.path.join(the_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(root_folder, os.path.relpath(index_path, root_folder))

        # 返回请求的文件
    return send_from_directory(root_folder, filename)


@app.route('/server/<path:path>')
def get_server_file(path):
    print("get_server_file", path)
    if not path.startswith("/"):
        path = "/" + path

    if not os.path.exists(path):
        abort(404)  # 如果文件不存在，返回404错误
    return send_file(path)


@app.route('/parse_folder', methods=['POST'])
def parse_folder():
    the_dict = request.json

    assert "id" in the_dict
    # 数据库中找到结果
    folder_obj = Folder.select().where(Folder.id == the_dict["id"])[0]
    folder_path = folder_obj.path

    assert os.path.exists(folder_path)
    # 数据库中找到结果

    # 转换为dict
    column = model_to_dict(folder_obj)

    # 1.寻找info.json
    info_path = os.path.join(folder_path, "info.json")

    if os.path.exists(info_path):
        with open(info_path, 'r') as name:
            info_file = json.load(name)
    else:
        info_file = None

    # 2.寻找name2text.json
    try:
        name2text_fp = os.path.join(folder_path, "name2text.json")
        assert os.path.exists(name2text_fp)
        name2text = json.load(open(name2text_fp, 'r'))
    except:
        name2text = {}

    # 获得所有wav文件
    file_names = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    file_names = sort_util.sort_files(file_names)

    # 得到全路径
    obj_list = []
    for name in file_names:
        obj = {
            'name': name,
            'path': os.path.join(folder_path, name),
            'info': {},
        }

        if name not in name2text:
            name2text[name] = ""

        try:
            for k, v in info_file['detail'][name].items():
                obj[k] = v
            for k, v in info_file['detail'][name].items():
                obj['info'][k] = v
        except:
            pass
        obj_list.append(obj)

    column['items'] = obj_list
    column['info'] = {}
    column['name2text'] = name2text
    if info_file is not None:
        if 'detail' in info_file:
            del info_file['detail']
        for key, value in info_file.items():
            column[key] = value

        for key, value in info_file.items():
            column['info'][key] = value

    return jsonify(column)


# @app.route('/parse_raw_folder', methods=['POST'])
# def parse_raw_folder():
#     the_dict = request.json
#     folder_path = the_dict["path"]
#     assert os.path.exists(folder_path)
#
#     # 获得所有wav文件
#     files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
#     # 按文件名排序
#     files = sort_util.sort_files(files)
#
#     info, detail_dict = info_parser.parse_info(folder_path)
#
#     # 得到全路径
#     obj_list = []
#     for name in files:
#         obj = {
#             'name': name,
#             'path': os.path.join(folder_path, name),
#             'info': detail_dict.get(name, None) if detail_dict else None
#         }
#         obj_list.append(obj)
#
#     return jsonify(
#         {"items": obj_list,
#          'name': folder_path.split("/")[-1],
#          'path': folder_path,
#          'info': info,
#          })


@app.route('/parse_ckpt_folder', methods=['POST'])
def parse_ckpt_folder():
    the_dict = request.json
    folder_path = the_dict["path"]
    assert os.path.exists(folder_path)

    # 获得所有.eval.json文件
    if not folder_path.endswith("/"):
        folder_path += "/"

    json_list = glob.glob(f"{folder_path}*.eval.json")
    jobj_list = [json_util.load_json(fp) for fp in json_list]
    jobj_list.sort(key=lambda x: x['step'])
    return jsonify({"list": jobj_list, })


@app.route('/new_folder', methods=['POST'])
def create_folder():
    # 1.读取原始数据
    the_dict = request.json
    folder_path = the_dict["path"]
    folder = Folder.create(
        name=folder_path.split("/")[-1],
        custom_name=the_dict.get("custom_name", ""),
        desc=the_dict.get("desc", ""),
        content_type=the_dict.get("content_type", 'wav'),
        path=folder_path,
    )
    return jsonify(model_to_dict(folder))


@app.route('/update_folder', methods=['POST'])
def update_folder():
    # 1.读取原始数据
    the_dict = request.json
    the_id = the_dict["id"]
    folder = Folder.get(Folder.id == the_id)
    fields = ['name', 'custom_name', 'desc', 'path', 'content_type']
    update_model_instance(folder, fields, the_dict)
    return jsonify(model_to_dict(folder))


@app.route('/update_name2text', methods=['POST'])
def update_name2text():
    # 1.读取原始数据
    the_dict = request.json
    the_path = the_dict["path"]
    name2text = the_dict["name2text"]
    json_util.save_json(os.path.join(the_path, 'name2text.json'), name2text)
    return jsonify({})


@app.route('/get_all_folder', methods=['POST'])
def get_all_folder():
    folder_list = list(Folder.select().order_by(Folder.created_date).dicts())[::-1]
    return jsonify(folder_list)


# =======================================================================================

@app.route('/new_collection', methods=['POST'])
def new_collection():
    the_dict = request.json
    new_collection = Collection.create(
        name=the_dict["name"],
        desc=the_dict.get("desc", ""),
        folder_order=the_dict.get("folder_order", ""),
        content_type=the_dict.get("content_type", "wav")
    )
    return jsonify(model_to_dict(new_collection))


@app.route('/update_collection', methods=['POST'])
def update_collection():
    the_dict = request.json
    the_id = the_dict["id"]
    col = Collection.get(Collection.id == the_id)
    fields = ['name', 'desc', 'folder_order', 'content_type']
    update_model_instance(col, fields, the_dict)
    return jsonify(model_to_dict(col))


@app.route('/get_all_collection', methods=['POST'])
def get_all_collection():
    the_list = list(Collection.select().order_by(Collection.created_date).dicts())
    return jsonify(the_list)


@app.route('/get_collection', methods=['POST'])
def get_collection():
    the_dict = request.json
    collection_id = the_dict["id"]
    c = Collection.get(Collection.id == collection_id)
    return jsonify(model_to_dict(c))


@app.route('/get_folders_of_collection', methods=['POST'])
def get_folders_of_collection():
    the_dict = request.json
    collection_id = the_dict["id"]

    collection = Collection.get(Collection.id == collection_id)
    folder_list = []
    if len(collection.folder_order) > 0:
        arr = json.loads(collection.folder_order)
        for i in arr:
            folder = Folder.get(Folder.id == i)
            folder = model_to_dict(folder)
            folder_list.append(folder)
    return jsonify(folder_list)


@app.route('/delete_collection', methods=['POST'])
def delete_collection():
    the_dict = request.json
    collection_id = the_dict["id"]
    collection = Collection.get(Collection.id == collection_id)
    collection.delete_instance()
    return jsonify({"status": "success", "message": f"Collection {collection_id} deleted"})


def update_model_instance(instance, model_fields, data_dict):
    for field_name in model_fields:
        if field_name in data_dict and field_name not in ['id']:
            setattr(instance, field_name, data_dict[field_name])
    instance.save()
