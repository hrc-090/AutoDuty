import os
from openpyxl import Workbook

def ensure_file_exists(file_path, template_func):
    """检查文件是否存在，不存在则创建"""
    if not os.path.exists(file_path):
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        wb = template_func()
        wb.save(file_path)
        print(f"已自动创建文件：{file_path}")
        return True
    return False

def create_duty_template():
    """创建值日表模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "值日表"
    # 设置首行
    ws.append(["星期", "扫地", "倒垃圾", "擦黑板"])
    # 设置后续几行示例
    ws.append(["周一", "张三", "李四", "王五"])
    ws.append(["周二", "赵六", "钱七", "孙八"])
    return wb

def create_alias_template():
    """创建别名表模板"""
    wb = Workbook()
    ws = wb.active
    ws.title = "别名表"
    # 设置首行
    ws.append(["中文名", "拼音别名"])
    # 设置后续几行示例
    ws.append(["张三", "zs_vip"])
    ws.append(["李四", "lisi_unique"])
    return wb