from openpyxl import load_workbook

def load_aliases(alias_file_path):
    """加载别名词典 {别名: 中文名}"""
    alias_dict = {}
    # 注意：这里不再检查文件是否存在，因为 main.py 已经确保文件存在或被创建
    # 但为了健壮性，仍保留 try-except 块
    try:
        # 再次检查，以防万一文件在 main.py 和此函数之间被意外删除
        import os # 在需要的地方导入
        if not os.path.exists(alias_file_path):
             print(f"警告：别名文件不存在，将仅使用拼音匹配。文件路径：{alias_file_path}")
             return alias_dict

        workbook = load_workbook(alias_file_path)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or not row[0] or not row[1]:
                continue
            zh_name = str(row[0]).strip()
            alias = str(row[1]).strip().lower()
            alias_dict[alias] = zh_name
    except FileNotFoundError:
        # 如果文件真的不存在，捕获这个特定异常
        print(f"警告：别名文件不存在，将仅使用拼音匹配。文件路径：{alias_file_path}")
    except Exception as e:
        print(f"读取别名文件出错: {e}")
    return alias_dict