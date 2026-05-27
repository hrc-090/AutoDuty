import json
import os

def load_config(config_path):
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_full_file_paths(config):
    """根据配置获取完整文件路径"""
    base_path = config['desktop_path']
    full_paths = {}
    for key, rel_path in config['files'].items():
        full_paths[key] = os.path.join(base_path, rel_path)
    return full_paths