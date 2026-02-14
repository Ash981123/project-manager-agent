README.md
项目管理Agent - GitHub Actions版
完全零安装！浏览器操作，永久免费！

方案说明
使用GitHub Actions的免费定时任务功能，每周一和周四自动运行脚本，发送飞书提醒。

优势
✅ 零安装 - 完全在浏览器中操作
✅ 零维护 - GitHub自动运行，无需电脑开机
✅ 永久免费 - GitHub Actions对公开仓库完全免费
✅ 稳定可靠 - 云端运行，不受网络影响
使用步骤
第一步：注册GitHub账号
访问 github.com
点击"Sign up"注册账号（如果已有账号可跳过）
第二步：创建仓库
登录GitHub后，点击右上角的"+"
选择"New repository"
填写信息：
Repository name: project-manager-agent
Description: 项目管理自动提醒
Public: 选择Public（公开仓库才能免费使用Actions）
点击"Create repository"
第三步：上传文件
方法一：通过网页上传（推荐）
在仓库页面，点击"Add file" → “Create new file”

第一个文件 - 工作流配置：

文件名输入：.github/workflows/reminder.yml
复制本项目中的 reminder.yml 内容粘贴进去
点击"Commit new file"
第二个文件 - Python脚本：

点击"Add file" → “Create new file”
文件名输入：github_action_script.py
复制本项目中的 github_action_script.py 内容粘贴进去
点击"Commit new file"
第三个文件 - 说明文档：

点击"Add file" → “Create new file”
文件名输入：README.md
复制本项目中的 README.md 内容粘贴进去
点击"Commit new file"
方法二：使用Git命令（如果你熟悉Git）
git clone https://github.com/你的用户名/project-manager-agent.git
cd project-manager-agent
# 复制本项目的文件到这里
git add .
git commit -m "初始化项目"
git push
第四步：配置密钥（重要！）
在你的GitHub仓库页面，点击"Settings"
左侧菜单选择"Secrets and variables" → “Actions”
点击"New repository secret"，逐个添加以下密钥：
密钥名称	值	说明
FEISHU_APP_ID	cli_xxxxxxxx	飞书应用的App ID
FEISHU_APP_SECRET	xxxxxxxxxxxxx	飞书应用的App Secret
FEISHU_APP_TOKEN	bascnxxxxxxxx	多维表格的App Token
FEISHU_TABLE_ID	tblxxxxxxxxxx	多维表格的Table ID
FEISHU_CHAT_ID	oc_xxxxxxxxxx	飞书群聊的Chat ID
如何获取这些信息？ 详见本文档末尾的"飞书配置指南"

第五步：启用Actions
在仓库页面，点击顶部的"Actions"标签
如果看到提示，点击"I understand my workflows, go ahead and enable them"
你会看到"项目管理提醒"工作流
第六步：测试运行
在Actions页面，点击左侧的"项目管理提醒"
点击右侧的"Run workflow"
点击绿色的"Run workflow"按钮
等待几秒钟，刷新页面
点击运行记录查看日志
如果成功，你会在飞书群里收到测试消息
完成！
现在系统会自动在：

每周一早上9点 发送本周任务清单
每周四早上9点 发送任务跟进
工作原理
GitHub Actions (云端)
  ↓
每周一、周四 9:00 自动触发
  ↓
运行 Python 脚本
  ↓
访问飞书多维表格 API → 获取本周任务
  ↓
发送卡片消息到飞书群聊
自定义提醒时间
编辑 .github/workflows/reminder.yml 文件：

on:
  schedule:
    # 每周一早上9点 (UTC时间1点 = 北京时间9点)
    - cron: '0 1 * * 1'
    # 每周四早上9点
    - cron: '0 1 * * 4'
时间计算： GitHub使用UTC时间，北京时间需要减8小时

北京时间 09:00 = UTC 01:00 → 0 1
北京时间 14:00 = UTC 06:00 → 0 6
北京时间 18:00 = UTC 10:00 → 0 10
Cron格式： 分钟 小时 日 月 星期

0 1 * * 1 = 每周一的UTC 01:00
0 1 * * 4 = 每周四的UTC 01:00
查看运行记录
访问仓库的"Actions"页面
点击具体的运行记录
查看详细日志
如果失败，检查错误信息
常见问题
Q1: 没有收到提醒？
检查清单：

Actions是否已启用？（仓库Settings → Actions → General → 允许Actions）
工作流是否运行成功？（查看Actions页面）
密钥是否正确配置？（Settings → Secrets）
飞书机器人是否在群里？
多维表格是否有本周任务？
Q2: 如何修改提醒时间？
编辑 .github/workflows/reminder.yml 中的 cron 表达式。

Q3: 能否发送给个人而不是群聊？
可以！修改密钥配置：

将 FEISHU_CHAT_ID 改为 FEISHU_USER_ID
值填写你的 Open ID
修改 github_action_script.py 中的发送逻辑（将 chat_id 改为 open_id）
Q4: Actions配额够用吗？
完全够用！

公开仓库：无限制
私有仓库：每月2000分钟
本项目每次运行约30秒，一个月8次，总共4分钟
Q5: 如何停止自动提醒？
临时停止：

进入仓库的Actions页面
点击左侧"项目管理提醒"
点击右上角"…"→“Disable workflow”
永久删除：
删除 .github/workflows/reminder.yml 文件

Q6: 可以添加更多提醒时间吗？
可以！在 reminder.yml 的 schedule 部分添加更多 cron 表达式：

schedule:
  - cron: '0 1 * * 1'  # 周一 9:00
  - cron: '0 1 * * 4'  # 周四 9:00
  - cron: '0 6 * * 5'  # 周五 14:00
飞书配置指南
获取 App ID 和 App Secret
访问 飞书开放平台
创建企业自建应用
在"凭证与基础信息"中查看
添加权限：bitable:app 和 im:message
发布应用版本
获取 App Token 和 Table ID
打开飞书多维表格
浏览器地址栏格式：
https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID&view=...
复制 APP_TOKEN 和 TABLE_ID
获取 Chat ID
将机器人添加到群聊
在开放平台的应用后台 → 机器人 → 调试
在群里@机器人发送消息
在调试日志中找到 chat_id
多维表格字段要求
字段名称	字段类型	选项
任务名称	文本	-
开始日期	日期	含时间
截止日期	日期	含时间
优先级	单选	高、中、低
状态	单选	待开始、进行中、已完成、已延期
描述	文本	-
技术支持
如有问题：

查看Actions运行日志
检查密钥配置是否正确
确认飞书应用权限已发布
在GitHub Issues中提问
祝使用愉快！ 🎉
