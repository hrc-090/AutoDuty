# 修改后的 main.py 文件
import os
import subprocess
import config_manager
import file_handler
import alias_manager
import duty_scheduler

def send_duty_notification(api_url, content):
    if not content:
        print("没有获取到值日信息，取消发送。")
        return
    command = f'curl -X POST {api_url} -d "{content}"'
    print(f"准备发送内容：{content}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 发送成功！")
        else:
            print(f"❌ 发送失败：{result.stderr}")
    except Exception as e:
        print(f"执行命令出错：{e}")

def main():
    print("--- 值日生自动填充与提醒程序启动（配置增强版）---")
    
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'config.json')
    config = config_manager.load_config(config_path)
    file_paths = config_manager.get_full_file_paths(config)

    # 检查并创建文件
    file_handler.ensure_file_exists(file_paths['duty_schedule'], file_handler.create_duty_template)
    file_handler.ensure_file_exists(file_paths['aliases'], file_handler.create_alias_template)

    alias_dict = alias_manager.load_aliases(file_paths['aliases'])
    
    # 自动填充值日表
    duty_scheduler.fill_duty_table_with_real_names(file_paths['duty_schedule'], alias_dict)

    # 使用新的配置项
    switch_hour = config.get('switch_time', 19)
    sunday_handling = config.get('sunday_handling', {
        'before_switch_time': 'get_prev_day',
        'after_switch_time': 'get_next_day'
    })
    
    weekday_num = duty_scheduler.get_target_weekday(switch_hour, sunday_handling)
    
    duty_text = duty_scheduler.read_duty_schedule_for_day(file_paths['duty_schedule'], weekday_num)
    send_duty_notification(config['api_url'], duty_text)

if __name__ == "__main__":
    main()