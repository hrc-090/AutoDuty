import os
from datetime import datetime, timedelta
from openpyxl import load_workbook, Workbook
from pypinyin import lazy_pinyin

def get_target_weekday(switch_hour, sunday_handling):
    """
    根据配置的切换时间，判断需要获取哪一天的值日安排
    :param switch_hour: 自动切换到下一天的小时数（整数）
    :param sunday_handling: 周日处理策略配置
    """
    now = datetime.now()
    current_weekday = now.weekday()
    target_date = now

    if current_weekday == 6:  # 周日特殊处理
        if now.hour >= switch_hour:
            # 周日过了切换时间，根据配置决定行为
            handling_type = sunday_handling.get('after_switch_time', 'get_next_day')
            if handling_type == 'get_next_day':
                target_date = now + timedelta(days=1)  # 获取周一
                print(f"当前是周日且已过 {switch_hour}:00，正在获取明天（周一）的值日安排...")
            elif handling_type == 'get_current_day':
                target_date = now  # 仍然是周日
                print(f"当前是周日且已过 {switch_hour}:00，正在获取今天的值日安排...")
            else:  # 默认行为
                target_date = now + timedelta(days=1)
                print(f"当前是周日且已过 {switch_hour}:00，正在获取明天（周一）的值日安排...")
        else:
            # 周日未到切换时间，根据配置决定行为
            handling_type = sunday_handling.get('before_switch_time', 'get_prev_day')
            if handling_type == 'get_prev_day':
                target_date = now - timedelta(days=1)  # 获取周六
                print(f"当前是周日且未到 {switch_hour}:00，正在获取周六的值日安排...")
            elif handling_type == 'get_current_day':
                target_date = now  # 仍然是周日
                print(f"当前是周日且未到 {switch_hour}:00，正在获取今天的值日安排...")
            elif handling_type == 'get_next_week_first_day':
                # 获取下周一
                target_date = now + timedelta(days=2)  # 从周日跳到下周一
                print(f"当前是周日且未到 {switch_hour}:00，正在获取下周一的值日安排...")
            else:  # 默认行为
                target_date = now - timedelta(days=1)
                print(f"当前是周日且未到 {switch_hour}:00，正在获取周六的值日安排...")
    else:
        if now.hour >= switch_hour:
            target_date = now + timedelta(days=1)
            print(f"当前已过 {switch_hour}:00，正在获取明天 ({target_date.strftime('%Y-%m-%d')}) 的值日安排...")
        else:
            target_date = now
            print(f"当前未到 {switch_hour}:00，正在获取今天 ({target_date.strftime('%Y-%m-%d')}) 的值日安排...")
    
    return target_date.weekday() + 1

def fill_duty_table_with_real_names(duty_file_path, alias_dict):
    if not os.path.exists(duty_file_path):
        print(f"错误：找不到值日表文件 {duty_file_path}")
        return

    try:
        workbook = load_workbook(duty_file_path)
        sheet = workbook.active
        
        updated_anything = False
        for row in sheet.iter_rows(min_row=2, values_only=False):
            for cell in row:
                if cell.value is not None and isinstance(cell.value, str):
                    original_value = cell.value.strip()
                    if original_value.lower() in alias_dict:
                        real_name = alias_dict[original_value.lower()]
                        cell.value = real_name
                        print(f"已将 '{original_value}' 替换为 '{real_name}'")
                        updated_anything = True
                    else:
                        for alias_key, real_name in alias_dict.items():
                            pinyin_full = "".join(lazy_pinyin(real_name)).lower()
                            pinyin_short = "".join([p[0] for p in lazy_pinyin(real_name)]).lower()
                            if original_value.lower() == pinyin_full or original_value.lower() == pinyin_short:
                                cell.value = real_name
                                print(f"已将拼音 '{original_value}' 替换为 '{real_name}'")
                                updated_anything = True
                                break
        if updated_anything:
            workbook.save(duty_file_path)
            print(f"值日表已更新并保存至 {duty_file_path}")
        else:
            print("本次运行未发现需要替换的拼音/别名。")

    except Exception as e:
        print(f"更新值日表时出错：{e}")

def read_duty_schedule_for_day(duty_file_path, weekday_num):
    weekday_map = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
    target_weekday = weekday_map.get(weekday_num)

    if not os.path.exists(duty_file_path):
        print(f"错误：在路径下找不到文件 {duty_file_path}")
        return ""

    duties = []
    try:
        workbook = load_workbook(duty_file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or str(row[0]).strip() != target_weekday:
                continue

            for i in range(1, len(headers)):
                person = row[i] if i < len(row) else ""
                if person and str(person).strip():
                    person_name = str(person).strip()
                    duties.append(f"{headers[i]}：{person_name}")
            break
    except Exception as e:
        print(f"读取值日表文件出错：{e}")
        return ""
    
    return "、".join(duties)

# 测试函数
def test_new_config_logic():
    print("=== 测试新的配置文件逻辑 ===")
    
    # 模拟不同的配置
    configs = [
        {
            "name": "原配置",
            "config": {
                "switch_time": 19,
                "sunday_handling": {
                    "before_switch_time": "get_prev_day",  # 获取周六
                    "after_switch_time": "get_next_day"    # 获取周一
                }
            }
        },
        {
            "name": "周日始终获取当天",
            "config": {
                "switch_time": 19,
                "sunday_handling": {
                    "before_switch_time": "get_current_day",  # 获取当天（周日）
                    "after_switch_time": "get_current_day"    # 获取当天（周日）
                }
            }
        },
        {
            "name": "周日前半段获取下周一",
            "config": {
                "switch_time": 19,
                "sunday_handling": {
                    "before_switch_time": "get_next_week_first_day",  # 获取下周一
                    "after_switch_time": "get_next_day"               # 获取周一
                }
            }
        }
    ]
    
    for cfg_info in configs:
        print(f"\n--- 测试配置: {cfg_info['name']} ---")
        config = cfg_info['config']
        
        # 模拟周日上午（未到切换时间）
        print("周日上午（未到切换时间）:")
        # 实际运行时会根据当前时间计算，这里只是展示逻辑
        print(f"  切换时间: {config['switch_time']}:00")
        print(f"  周日未到切换时间时的行为: {config['sunday_handling']['before_switch_time']}")
        print(f"  周日过了切换时间时的行为: {config['sunday_handling']['after_switch_time']}")

if __name__ == "__main__":
    test_new_config_logic()