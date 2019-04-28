import util
import time,datetime
import sched
import schedule

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import traceback

import random

mail_host="smtp.126.com"  # 设置服务器
mail_user="fuyingdi"    # 用户名
mail_pass="furuanmei64325"   # 授权码
sender = 'fuyingdi@126.com'
receivers = ['fuyingdi@126.com']  # 接收邮件


seat_ids = ['101439246', '101439247', '101439234','101439235'] # 一阅201 202 101 105
seat_id = seat_ids[0]
start_time = '7:00'
end_time = '22:00'

def get_dev_name():
    return util.get_resv_info()['devName']


def sendmail(subject, content):
    print("发送邮件: "+content)
    message = MIMEText(content)
    message['From'] = Header('Me', 'utf-8')
    message['To'] = Header('You', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功...')
    except:
        traceback.print_exc()
        print('邮件发送失败')


def job_get_seat():
   # time.sleep(random.randint(0, 3)*60+random.randint(0, 60))
    # 时间是否在6:00-22:00
    if time.localtime(time.time()).tm_hour <= 5 or time.localtime(time.time()).tm_hour >= 21:
        pass
    else:
        _index = 0
        global seat_id
        global start_time
        start_time = str(time.localtime(time.time()).tm_hour+1)+':00'
        while True:
            time.sleep(5)
            util.login()
            _info = util.get_resv_info()
            if _info is not None:
                print('已有预约{}'.format(_info['devName']))
                break 
            if util.occupy(seat_id, start_time, end_time):
                time.sleep(5)
                dev_name = get_dev_name()
                sendmail('已预约{},时间:{}-{}'.format(dev_name, start_time, end_time), '')
                break
            else:
                # sendmail('预约{}失败'.format(''), str(time.asctime(time.localtime(time.time()))))
                if _index != len(seat_ids) -1:
                    _index +=1
                    seat_id = seat_ids[_index]
                else:
                    seat_id = util.check_empty(start_time, end_time)
                


def job_update_seat(mode):
    time.sleep(random.randint(0, 3)*60+random.randint(0, 60))
    print("UPDATE")
    # 时间是否在6:00-22:00
    if time.localtime(time.time()).tm_hour < 6 or time.localtime(time.time()).tm_hour >= 21:
        pass
    else:
        # 取得当前座位的id
        while True:
            global seat_id
            util.login()
            _info = util.get_resv_info()
            if _info is not None:
                seat_id = _info['devId']
                print('确认更新，座位ID为：{}'.format(seat_id))
                break
            time.sleep(1) 
        try:    
            util.login()
            _dev_name = get_dev_name()
            util.delet_seat()
            time.sleep(10)
            sendmail('已取消预约{}'.format(_dev_name), time.asctime(time.localtime(time.time())))
        except:
            sendmail('!!!!!!!!!!!!取消失败，请手动取消预约!!!!!!!!!!!!!!!!', '')
        time.sleep(30)
        # 重新预约一小时后
        global start_time
        retry = 10
        while retry>0:
            if mode == 1:
                start_time = str(time.localtime(time.time()).tm_hour + 1) +':00' # 在9:25分修改成10:00
            elif mode == 2:
                start_time = str(time.localtime(time.time()).tm_hour + 1) +':30' # 在9:55分修改成10:30
            print(seat_id, start_time, end_time)
            if util.occupy(seat_id, start_time, end_time):
                sendmail('已重新预约:{},时间{}-{}'.format(_dev_name, start_time, end_time), time.asctime(time.localtime(time.time())))
                print('重新预约成功')                
                break
            time.sleep(3)
            retry -= 1


def start():
    schedule.every().day.at("06:30").do(job_get_seat)
    schedule.every().hour.at(":25").do(job_update_seat, mode=1)
    schedule.every().hour.at(":55").do(job_update_seat, mode=2)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
      #  print(schedule.next_run(),schedule.idle_seconds())

if __name__ == '__main__':
    job_get_seat()
#    job_update_seat(1)
    start()

