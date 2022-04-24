# XQT-Clockin-Practice
校企通-多用户自动打卡

> 2022.04.24 -> 支持实习自动签到

---

## 一、本地运行

### 1. 安装依赖

- `pip install -r requirements.txt`

### 2. 添加需要自动打卡的用户

1. 修改`idlist_sample.csv`为`idlist.csv`
2. 按照`idlist.csv`格式添加用户信息，除`remark`字段为非必填外，其余字段必填，否则将导致自动打卡失败

### 3. 运行自动化打卡脚本

- `python3 clockin.py`

## 二、云函数托管运行

...todo...

## 三、更新日志

- [点击查看更新日志](./UpdateLog.md)

## 四、其它问题

- 欢迎提issue
- 欢迎PR
- 喜欢的话给个star喵~
