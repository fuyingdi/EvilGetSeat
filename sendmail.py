import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.126.com"  # 设置服务器
mail_user = "fuyingdi"  # 用户名
mail_pass = "furuanmei64325"  # 授权码
sender = 'fuyingdi@126.com'
receivers = ['fuyingdi@126.com']  # 接收邮件




def sendmail(subject, content):
    print("发送邮件: " + content)
    message = MIMEText(content)
    message['From'] = Header('Me', 'utf-8')
    message['To'] = Header('You', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功...')
    except:
        print('邮件发送失败')
