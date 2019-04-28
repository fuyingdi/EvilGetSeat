"""
用魔鬼的方法占用图书馆的座位
"""

import requests
import json
import pprint
import time
import sys


user_id = '160104010116'
password = '124563'

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
                      'room_id={}&date={}&act=get_rsv_sta' \
                      '&fr_start={}&fr_end={}&_nocache=1534047543589'

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
        return True
    else:
        return False


def relogin():
    # 刷新登陆状态，若不成功，重新登陆
    data = evil_session.get(relogin_url)
    data = json.loads(data.text)
    print(data)
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
    if _data['ret'] == 1:
        if len(_data['data']) > 0:
            result = _data['data'][0]
            return result
        else:
            return None


# 占座
def occupy(seat_id, start_time, end_time):
    resv_id = ''
    dev_id = seat_id
    lab_id = ''
    # start = '2019-04-14 15:30'
    start = time.strftime("%Y-%m-%d", time.localtime()) + " " + start_time
    end = time.strftime("%Y-%m-%d",time.localtime()) + " " + end_time
    response = evil_session.get(occupy_url.format(dev_id=dev_id, lab_id=lab_id, start=start, end=end, resv_id=resv_id))
    print(response.text)
    response = json.loads(response.text)
    if response['ret'] == 1:
        return True
    else:
        return False


def delet_seat():
    # 删除当前的预约
    print("尝试删除预约...")
    try:
        resv_id = get_resv_info()['id']
        _del_resv_url = del_resv_url.format(resv_id)

        # 刷新登陆状态
        if relogin():
            response = evil_session.get(_del_resv_url)
            print(response.text)
        else:
            login()
            response = evil_session.get(_del_resv_url)
            print(response.text)
    except:
        print("重新登陆失败")


def check_empty(startime,endtime):
    # 查询空座
    room_id = '100457211'
    date = time.strftime("%Y-%m-%d", time.localtime())

    _url = get_room_status_url.format(room_id, date, startime, endtime)
    response = evil_session.get(_url)
    data = json.loads(response.text)

    if data['ret'] == 1:
        seats = data['data']
        for seat in seats:
            if len(seat['ts']) == 0:
                print("找到空座:" + seat['devName'])
                return str(seat['id']).split('_')[0]


if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1] == '-o':
            login()
            print("正在占座，时间：{}->{}".format(sys.argv[2], sys.argv[3]))
            try:
                seat_id = check_empty(sys.argv[2], sys.argv[3])
                occupy(seat_id, sys.argv[2], sys.argv[3])
            except:
                pass
        else:
            print(sys.argv)
    else:
        check_empty('18:00', '22:00')


    '''
    login()
    resv_info = get_resv_info()
    print(resv_info)
    print("查询预约信息...")
    print("正在占座...")
    # occupy("15:00", "16:30")
    delet_seat()
'''
