"""
html邮件的发送
version 1.1.0
author lkk
email lkk199404@163.com
DESC: 发送带附件
"""

import os
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
# 引入依赖的模块
from smtplib import SMTP_SSL


def __format_site(user):
    re, site = parseaddr(user)
    return formataddr((Header(re, "utf-8").encode(), site))


# 定义发件人信息
SMTP_SERVER = 'smtp.yandex.ru'
EMAIL_USER = 'xyongqiang@yandex.com'
EMAIL_PASS = 'xyq123456'

# 定义收件人、发件人
sender = EMAIL_USER
receiver = 'hanellinnepo-2338@yopmail.com'

#定义邮件对象
message = MIMEMultipart()

# 绑定发件人、收件人、主题
message['from'] = sender
message['to'] = receiver
message['subject'] = Header('Code navigation is available', 'utf-8')

# 定义信件文本内容
content = MIMEText(
    'Navigate your code with ease. Click on function and method calls to jump to their definitions or references in the same repository. Learn more',
    'plain', 'utf-8')
message.attach(content)

BOOKPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'download', '莽荒纪.txt')

print('BOOKPATH->%s' % BOOKPATH)

# 绑定一个附件
with open(BOOKPATH, 'rb') as f:
    # 设置MIMEBase对象包装附件
    attachment = MIMEBase('text', 'txt', filename='莽荒纪.txt')  # MIMEBase('application', 'octet-stream')
    # 添加附件
    attachment.set_payload(f.read())
    # 添加附件标题
    print('f.name->%s' % f.name)
    # attachment.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', '莽荒纪.txt'))
    # 加上必要的头信息:
    attachment.add_header('Content-Disposition', 'attachment', filename='莽荒纪.txt')
    attachment.add_header('Content-ID', '<0>')
    attachment.add_header('X-Attachment-Id', '0')
    # 编码附件
    encoders.encode_base64(attachment)
    # 添加附件到邮件中
    message.attach(attachment)

# 登录邮件服务器
mail_server = SMTP_SSL(SMTP_SERVER, 465)
mail_server.set_debuglevel(1)
mail_server.login(EMAIL_USER, EMAIL_PASS)
# 发送邮件
mail_server.sendmail(from_addr=sender, to_addrs=[sender], msg=message.as_string())

# 发送完成
mail_server.quit()
print('邮件已发送>>>>')
