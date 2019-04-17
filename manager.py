import util
import time,datetime
import sched
import schedule

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import traceback

import random

mail_host="smtp.qq.com"  # 设置服务器
mail_user="719309759"    # 用户名
mail_pass="svxdbzghgfrtbdih"   # 授权码
sender = '719309759@qq.com'
receivers = ['fuyingdi@126.com']  # 接收邮件


seat_id = '101439246'  # 一阅201
tart_time = '6:30'
end_time = '22:00'


def sendmail(subject, content):
    print("发送邮件: "+content)
    message = MIMEText(content)
    message['From'] = Header('Me', 'utf-8')
    message['To'] = Header('You', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功...')
    except:
        traceback.print_exc()
        print('邮件发送失败')


def job_get_seat():
    time.sleep(random.randint(0, 10)*60+random.randint(0, 60))
    # 时间是否在6:00-22:00
    if time.localtime(time.time()).tm_hour <= 5 or time.localtime(time.time()).tm_hour >= 22:
        pass
    else:
        global start_time
        util.login()
        if util.occupy(seat_id, start_time, end_time):
            sendmail('已预约一阅201,时间：' + "{}-{}".format(start_time, end_time), '')
            start_time = str(time.localtime(time.time()).tm_hour + 1) + ':30'
        else:
            sendmail('预约失败', '')


def job_cancel_seat():
    time.sleep(random.randint(0, 10)*60+random.randint(0, 60))
    # 时间是否在6:00-22:00
    if time.localtime(time.time()).tm_hour <= 7 or time.localtime(time.time()).tm_hour >= 22:
        pass
    else:
        util.login()
        util.delet_seat()
        sendmail('已取消预约', '')


def start():
    schedule.every().hour.at(":31").do(job_cancel_seat)
    schedule.every().hour.at(":01").do(job_cancel_seat)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    start()
