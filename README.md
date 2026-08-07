[readme.md](https://github.com/user-attachments/files/28324393/readme.md)
> [!IMPORTANT]
>  **该项目已废弃**

> [!IMPORTANT]
> **温馨提示**：本项目代码由**氛围编程 (Vibe Coding)** 方式编写。

# 值日安排自动化管理系统

## 系统概述

这是一个自动化的值日安排管理系统，支持别名映射、智能拼音识别、定时切换和自动通知功能。系统可以根据时间自动获取对应的值日安排，并通过API接口发送通知。

## 功能特性

- **Excel文件管理**: 从Excel文件读取值日安排和别名词典
- **智能姓名映射**: 支持别名和拼音自动转换为真实姓名
- **定时切换**: 根据配置时间自动获取当天或明天的值日安排
- **周日特殊处理**: 可配置的周日处理逻辑
- **自动通知**: 通过API发送值日提醒
- **模板创建**: 自动创建缺失的Excel模板文件

## 文件结构
├── main.py                 # 主程序入口
├── config.json             # 系统配置文件
├── config_manager.py       # 配置管理模块
├── alias_manager.py        # 别名词典管理模块
├── duty_scheduler.py       # 值日调度模块
├── file_handler.py         # 文件处理模块
└── data/                   # 数据文件目录
    ├── 值日表.xlsx         # 值日安排表
    └── aliases.xlsx        # 别名词典表
```

## 配置文件说明

### config.json 配置项

```json
{
  "api_url": "http://localhost:36000/durty",
  "desktop_path": ".",
  "switch_time": 19,
  "sunday_handling": {
    "before_switch_time": "get_prev_day",
    "after_switch_time": "get_next_day"
  },
  "files": {
    "duty_schedule": "data\\值日表.xlsx",
    "aliases": "data\\aliases.xlsx"
  }
}
```

### 配置项详细说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `api_url` | 字符串 | - | 接收通知的API端点 |
| `desktop_path` | 字符串 | "." | 基础路径 |
| `switch_time` | 数字 | 19 | 自动切换到下一天的时间（小时） |
| `sunday_handling.before_switch_time` | 字符串 | "get_prev_day" | 周日未到切换时间时的行为 |
| `sunday_handling.after_switch_time` | 字符串 | "get_next_day" | 周日过了切换时间时的行为 |

### Sunday Handling 行为选项

- `get_prev_day`: 获取前一天的值日安排
- `get_current_day`: 获取当天的值日安排
- `get_next_day`: 获取下一天的值日安排
- `get_next_week_first_day`: 获取下周第一天的值日安排

## 数据文件格式

### 值日表.xlsx
| 星期 | 扫地 | 倒垃圾 | 擦黑板 |
|------|------|--------|--------|
| 周一 | 张三 | 李四 | 王五 |
| 周二 | 赵六 | 钱七 | 孙八 |

### aliases.xlsx
| 中文名 | 拼音别名 |
|--------|----------|
| 张三 | zs_vip |
| 李四 | lisi_unique |

## 安装依赖

```bash
pip install openpyxl pypinyin
```

## 使用方法

1. **配置系统**
   - 编辑 `config.json` 文件，设置正确的API URL和其他配置

2. **准备数据文件**
   - 系统会自动创建缺失的Excel模板文件
   - 手动编辑 `data/值日表.xlsx` 添加值日安排
   - 手动编辑 `data/aliases.xlsx` 添加姓名映射关系

3. **运行系统**
   ```bash
   python main.py
   ```

## 工作流程

1. 检查并创建必要的Excel文件
2. 加载别名词典进行姓名映射
3. 根据当前时间和配置决定获取哪天的安排
4. 更新值日表中的别名为真实姓名
5. 读取值日安排并通过API发送通知

## 特殊处理逻辑

### 时间切换逻辑
- **平时**: 如果当前时间 ≥ 切换时间，则获取明天的安排；否则获取今天的安排
- **周日**:
  - 未到切换时间: 根据配置获取前一天/当天/下一天
  - 已过切换时间: 根据配置获取前一天/当天/下一天

### 姓名匹配逻辑
1. 首先尝试精确匹配别名词典
2. 然后尝试匹配全拼或简拼
3. 支持大小写不敏感匹配

## 注意事项

- 确保API服务正常运行
- Excel文件路径必须正确
- 值日表和别名词典需要按照指定格式填写
- 系统会在首次运行时自动创建模板文件

## 故障排除

### 常见问题
1. **文件不存在**: 系统会自动创建模板，手动添加数据即可
2. **API发送失败**: 检查网络连接和API端点配置
3. **姓名未匹配**: 检查别名词典中的映射关系

### 日志输出
系统会输出详细的处理过程，便于调试和监控

## 扩展性

系统采用模块化设计，易于扩展：
- 可以轻松修改时间切换逻辑
- 支持多种通知方式（只需修改 `send_duty_notification` 函数）
- 配置灵活，适应不同场景需求
```
