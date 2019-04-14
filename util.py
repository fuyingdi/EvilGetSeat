"""
用魔鬼的方法占用图书馆的座位
"""

import requests
import json
import pprint
import time


user_id = '160104010116'
password = '124563'

room_id = ''
date = ''
resv_id = ''

headers = {}

login_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/login.aspx?' \
            'act=login&id={}&pwd={}&role=512&aliuserid=&schoolcode=&wxuserid=&_nocache=1531731958096'.format(
                user_id, password)
relogin_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/login.aspx?' \
              'act=login&id=@relogin&pwd=&role=512&aliuserid=&schoolcode=&wxuserid=&_nocache=1541949437657'

get_resvid_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?' \
                 'stat_flag=9&act=get_my_resv&_nocache=1531801794371'

get_room_status_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/device.aspx?' \
                      'room_id={}&date={}'.format(room_id, date)

del_resv_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?' \
             'act=del_resv&id={}&_nocache=1531823241100' #.format(del_resv_id)

occupy_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?' \
             'dev_id={dev_id}&lab_id={lab_id}&room_id=&kind_id=&type=dev' \
             '&prop=&test_id=&resv_id={resv_id}&term=&min_user=&max_user=' \
             '&mb_list=&test_name=&start={start}&end={end}&memo=&act=set_resv&_nocache=1531732522498'

evil_session = requests.Session()


def login():
    # 登录
    data = evil_session.get(login_url)
    with open('data.txt', 'w+') as datafile:
        datafile.write(str(data.text))
    data = json.loads(data.text)
    if data['ret'] == 1:
        print('登录成功')
    else:
        return False


def relogin():
    # 刷新登陆状态，若不成功，重新登陆
    data = evil_session.get(relogin_url)
    data = json.loads(data.text)
    if data['ret'] == 1:
        print("刷新登陆状态成功")
        return True
    else:
        print("刷新登陆状态不成功，尝试重新登陆...")
        if login():
            return True
        else:
            return False


# 获取预约信息
def get_resv_info():
    _data = evil_session.get(get_resvid_url)
    _data = json.loads(_data.text)
    print(_data)
    if _data['ret'] == 1:
        return _data['data'][0]['id']


# 占座
def occupy(start_time, end_time):
    resv_id = ''
    dev_id = '101439235'
    lab_id = ''
    # start = '2019-04-14 15:30'
    start = time.strftime("%Y-%m-%d", time.localtime()) + " " + start_time
    end = time.strftime("%Y-%m-%d",time.localtime()) + " " + end_time
    response = evil_session.get(occupy_url.format(dev_id=dev_id, lab_id=lab_id, start=start, end=end, resv_id=resv_id))
    print(response.text)
    response = json.loads(response.text)
    pprint.pprint(response)


def delet_seat():
    # 删除当前的预约
    print("尝试删除预约...")
    resv_id = get_resv_info()
    _del_resv_url = del_resv_url.format(resv_id)

    # 刷新登陆状态
    if relogin():
        response = evil_session.get(_del_resv_url)
        print(response.text)
    else:
        print("重新登陆失败")


if __name__ == '__main__':
    login()
    resv_info = get_resv_info()
    print(resv_info)
    print("查询预约信息...")
    print("正在占座...")
    # occupy("15:00", "16:30")
    delet_seat()

