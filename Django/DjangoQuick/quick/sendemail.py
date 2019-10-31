"""
文本邮件的发送
version 1.1.0
author lkk
email lkk199404@163.com
"""
# 引入要用到的模块
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from smtplib import SMTP_SSL

import email, smtplib

# 定义发送人邮箱信息
SMTP_SERVER = 'smtp.yandex.ru'
EMAIL_USER = 'xyongqiang@yandex.com'
EMAIL_PASS = 'xyq123456'

# 定义发件人、收件人邮箱
sender = EMAIL_USER
receiver = 'larreddirut-7792@yopmail.com'

# 定义邮件内容
message = MIMEText(
    "Navigate your code with ease. Click on function and method calls to jump to their definitions or references in the same repository. Learn more",
    "plain", "utf-8")
# 定义收件人、发件人和邮件主题、如果不定义~可能会引发554垃圾邮件的检查错误
message['subject'] = Header('《脑筋急转弯》', 'utf-8')
message['from'] = sender
message['to'] = receiver

# 连接邮件服务器
server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
# 设置信息展示级别
server.set_debuglevel(1)
# 登录邮箱服务器
server.login(EMAIL_USER, EMAIL_PASS)
# 发送邮件

server.sendmail(sender, [receiver], message.as_string())

# 退出并关闭客户端
server.quit()
print("邮件发送结束.")
