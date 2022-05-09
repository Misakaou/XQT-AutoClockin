<div align="center">

# XQT-AutoClockin
## 校企通-自动打卡

[![BloveDawn - XQT-AutoClockin](https://img.shields.io/static/v1?label=BloveDawn&message=XQT-AutoClockin&color=blue&logo=github)](https://github.com/BloveDawn/XQT-AutoClockin "Go to GitHub repo")[![GitHub tag](https://img.shields.io/github/tag/BloveDawn/XQT-AutoClockin?include_prereleases=&sort=semver&color=blue)](https://github.com/BloveDawn/XQT-AutoClockin/releases/)[![GitHub release](https://img.shields.io/github/release/BloveDawn/XQT-AutoClockin?include_prereleases=&sort=semver&color=blue)](https://github.com/BloveDawn/XQT-AutoClockin/releases/)[![License](https://img.shields.io/badge/License-GPL--3.0-blue)](#license)
[![Run Auto Clockin](https://github.com/BloveDawn/XQT-AutoClockin/workflows/Run%20Auto%20Clockin/badge.svg)](https://github.com/BloveDawn/XQT-AutoClockin/actions?query=workflow:"Run+Auto+Clockin")[![issues - XQT-AutoClockin](https://img.shields.io/github/issues/BloveDawn/XQT-AutoClockin)](https://github.com/BloveDawn/XQT-AutoClockin/issues)
[![stars - XQT-AutoClockin](https://img.shields.io/github/stars/BloveDawn/XQT-AutoClockin?style=social)](https://github.com/BloveDawn/XQT-AutoClockin)[![forks - XQT-AutoClockin](https://img.shields.io/github/forks/BloveDawn/XQT-AutoClockin?style=social)](https://github.com/BloveDawn/XQT-AutoClockin)

校企通-多用户自动打卡

> 2022.04.24 -> 支持实习自动签到

</div>

---

## 一、本地运行

### 1. 克隆本存储库到本地

- `git clone https://github.com/BloveDawn/XQT-AutoClockin.git`

### 2. 安装依赖

- `cd XQT-AutoClockin`
- `pip install -r requirements.txt`

### 3. 添加需要自动打卡的用户

1. 重命名`idlist_sample.csv`为`idlist.csv`
2. 按照`idlist.csv`格式添加用户信息，除`remark`字段为非必填外，其余字段必填，否则将导致自动打卡失败
3. 重命名`config_sample.conf`为`config.conf`，请勿修改此文件除`email`节外的任意一节，否则将导致自动打卡失败

### 4. 运行自动化打卡脚本

- `python3 RunClockin.py`

> ### 其他功能
>
> #### 1. 开启邮件发送服务(可选)(不推荐，可能会被邮件服务器屏蔽)
>
> - 自行修改`config.conf`文件中的`email`节中的内容，`enabled = true`为开启服务

---

## 二、Github Action 自动运行

> **注意：**
>
> 如果您选择以此方式运行，由于公开仓库的GithubAction的日志是可见的，而且本程序会在日志中输出您的用户信息，所以程序将会自动屏蔽标准输出日志。希望以此方式运行的用户，请配置邮箱地址，以便接收日志信息，否则您的所有日志将会被销毁。

### 1. Fork本仓库

- [点击以Fork](https://github.com/BloveDawn/XQT-AutoClockin/fork)

### 2. 配置仓库私有环境变量

1. 打开仓库设置页面，点击`Secrets`，点击`Actions`
2. 点击`New repository secret`添加私有环境变量，**注意：就算不填也全部必须创建，否则将会运行失败**
   1. 添加配置是否启用GithubAction服务
      - Name: `ACTION_ENABLED`
      - Value: `true`或者`false`
   2. 添加自动打卡用户配置
      - Name: `CLOCKIN_USERS`
      - Value:**注意：请勿随意增添空格，否则打卡那边查无此人、查无此地**
         ```text
         id,phone,province,city,district,address,email,remarks
         140502200000000001,19899999999,山西省,太原市,小店区,山西省太原市小店区CD写字楼,a@b.com,张三
         140502200000000002,19899999999,山西省,临汾市,尧都区,山西省临汾市尧都区AB写字楼,c@d.com,李四
         ```
      - 备注：将`idlist_sample.csv`中所有内容原封不动复制过来，再进行修改
   3. 添加邮件配置
      - Name: `EMAIL_ENABLED`
      - Value: `true`或者`false`
      - Name: `EMAIL_SMTP_HOST`
      - Value: `smtp.qq.com`
      - Name: `EMAIL_SMTP_PORT`
      - Value: `465`
      - Name: `EMAIL_SMTP_ADDRESS`
      - Value: `your_sender_email@example.org`
      - Name: `EMAIL_SMTP_PASSWORD`
      - Value: `your_sender_email_password`
      - Name: `EMAIL_SMTP_RECEIVER_LIST`
      - Value: `[your_reciver_email@example.org,your_reciver_email2@example.org]`(重要提示：请勿随意添加空格)
      - Name: `EMAIL_SEND_LOG_LEVEL`
      - Value: `info`或者`warning`(推荐)或者`error`

### 3. 启用GithubAction服务

- 在您fork的仓库的Action页面中启用`Run Auto Clockin`服务

---

## 三、云函数托管运行

### 1. 阿里云函数

#### 1) ALIYUNFC-创建云函数

1. [点击进入阿里云函数FC控制台](https://fcnext.console.aliyun.com/)
2. 点击左侧边栏中的[**服务及函数**
3. 在**服务列表**中点击**创建服务**，随便填写一个名称，剩余保持默认即可
4. 点击进入刚刚创建的服务
5. 点击**创建函数**，选择`从零开始创建`
   1. 基本设置
      1. 函数名称：随便填写
      2. 运行环境：`Python3.9`
      3. 请求处理程序类型：`处理事件请求`
      4. 实例类型：`弹性实例`
      5. 内存规格：`128MB`
   2. 配置触发器
      1. 触发器类型：`定时触发器`
      2. 名称：随意填写
      3. 触发方式：`指定时间`
      4. 时区：`Asia/Shanghai`
      5. 指定时间：`9:00:00`
      6. 指定日期：留空
      7. 指定星期：留空
      8. 触发消息：随便填写
6. 点击**创建**，完成函数创建

#### 2) ALIYUNFC-上传代码&修改用户信息

1. 进入刚刚创建的函数详情页面，等待函数代码加载完成，等待终端加载完成
2. [点击下载本项目代码](https://github.com/BloveDawn/XQT-AutoClockin/archive/refs/heads/main.zip)到本地并解压缩
3. 点击函数详情页面的**上传代码**，选择**上传文件夹**，选择**选择文件夹**，随后选择您解压好的代码文件，点击**上传**，选中**我想在上传完成后直接部署函数**，点击**保存并部署**
4. 重命名`idlist_sample.csv`为`idlist.csv`
5. 按照`idlist.csv`格式添加用户信息，除`remark`字段为非必填外，其余字段必填，否则将导致自动打卡失败，**注意，该填的逗号不能省略，否则将读取错位**
6. 重命名`config_sample.conf`为`config.conf`，请勿修改此文件除`email`节外的任意一节，否则将导致自动打卡失败

#### 3) ALIYUNFC-安装依赖

1. 在**在线IDE**的**终端**中输入命令`pip install -r requirements.txt -t .`安装依赖包，等待依赖包安装完成
2. 点击**部署代码**，完成函数代码部署

#### 4) ALIYUNFC-测试函数 (可选)

1. 点击**测试函数**，查看在线IDE上方函数日志窗口，检查函数是否正常运行

---

## 三、更新日志

- [点击查看更新日志](./UpdateLog.md)

## 四、其它问题

- 有任何问题欢迎到讨论区来讨论
- 欢迎提issue
- 欢迎PR
- 喜欢的话给个star喵~

## 五、依赖包

[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![dependency - pycryptodome](https://img.shields.io/badge/dependency-pycryptodome-blue)](https://pypi.org/project/pycryptodome)[![dependency - PyYAML](https://img.shields.io/badge/dependency-PyYAML-blue)](https://pypi.org/project/PyYAML)[![dependency - requests](https://img.shields.io/badge/dependency-requests-blue)](https://pypi.org/project/requests)
