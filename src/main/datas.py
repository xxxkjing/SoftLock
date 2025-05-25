import json
import os
import sys


# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(sys.executable), 'data.json')

# 初始化数据文件
def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)

# 加载数据
def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# 保存数据
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# 添加或更新数据
def add_data(file_path, strategy_id, additional_params):
    data = load_data()
    found = False
    for item in data:
        if item["file_path"] == file_path:
            # 如果找到相同的 file_path，更新该条目
            item["strategy_id"] = strategy_id
            item["additional_params"] = additional_params
            found = True
            break
    if not found:
        # 如果没有找到，添加新的条目
        data.append({
            "file_path": file_path,
            "strategy_id": strategy_id,
            "additional_params": additional_params
        })
    save_data(data)

# 修改数据
def modify_data(index, file_path=None, strategy_id=None, additional_params=None):
    data = load_data()
    if index < 0 or index >= len(data):
        print("Invalid index")
        return
    if file_path is not None:
        data[index]["file_path"] = file_path
    if strategy_id is not None:
        data[index]["strategy_id"] = strategy_id
    if additional_params is not None:
        data[index]["additional_params"] = additional_params
    save_data(data)

# 删除数据
def delete_data(index):
    data = load_data()
    if index < 0 or index >= len(data):
        print("Invalid index")
        return
    del data[index]
    save_data(data)

# 调用数据
def get_data(index):
    data = load_data()
    if index < 0 or index >= len(data):
        print("Invalid index")
        return None
    return data[index]

# 初始化数据文件
initialize_data_file()

# 按照文件路径查找数据
def find_data(file_path):
    data = load_data()
    for index, item in enumerate(data):
        if item["file_path"] == file_path:
            return data[index]
    return None

# 按文件路径查找并删除对应数据（取消加密）
def find_and_delete_data(file_path):
    data = load_data()
    for index, item in enumerate(data):
        if item["file_path"] == file_path:
            delete_data(index)
