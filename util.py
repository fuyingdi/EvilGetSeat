"""
用魔鬼的方法占用图书馆的座位
"""

import requests
import json
import time
import sys

user_id = '160104010116'
password = '124563'

date = ''
resv_id = ''

headers = {}

login_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/login.aspx?act=login&id={}&pw' \
            'd={}&role=512&aliuserid=&schoolcode=&wxuserid=&_nocache=1531731958096'.format(user_id, password)

relogin_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/login.aspx?' \
              'act=login&id=@relogin&pwd=&role=512&aliuserid=&schoolcode=&wxuserid=&_nocache=1541949437657'

get_resvid_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?' \
                 'stat_flag=9&act=get_my_resv&_nocache=1531801794371'

get_room_status_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/device.aspx?room_id={}&date={}&act=get_rsv_sta' \
                      '&fr_start={}&fr_end={}&_nocache=1534047543589'

del_resv_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?' \
               'act=del_resv&id={}&_nocache=1531823241100'  # .format(del_resv_id)

occupy_url = 'http://seat.ysu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?dev_id={dev_id}&lab_id={lab_id}&room_id=&kin' \
             'd_id=&type=dev&prop=&test_id=&resv_id={resv_id}&term=&min_user=&max_user=&mb_list=&test_name=&start={sta' \
             'rt}&end={end}&memo=&act=set_resv&_nocache=1531732522498'

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
        return False


# 获取预约信息
def get_resv_info():
    login()
    _data = evil_session.get(get_resvid_url)
    _data = json.loads(_data.text)

    if _data['ret'] == 1:
        if len(_data['data']) > 0:
            return _data['data'][0]
        else:
            return None


# 占座
def occupy(seat_id, start_time, end_time):
    login()

    start = time.strftime("%Y-%m-%d", time.localtime()) + " " + start_time
    end = time.strftime("%Y-%m-%d", time.localtime()) + " " + end_time

    response = evil_session.get(occupy_url.format(dev_id=seat_id, lab_id='', start=start, end=end, resv_id=''))

    response = json.loads(response.text)
    if response['ret'] == 1:
        print('占座成功')
        return True
    else:
        print('占座失败')
        return False


#  删除指定的预约
def delete_seat_with_id(_resv_id):
    _del_resv_url = del_resv_url.format(_resv_id)  # 拼接url
    # 刷新登陆状态
    if relogin():
        response = evil_session.get(_del_resv_url)
        _data = json.loads(response.text)
    else:
        login()
        response = evil_session.get(_del_resv_url)
    _data = json.loads(response.text)
    if _data['ret'] == 1:
        print('删除成功')
        return True
    else:
        print('删除失败')
        return False


# 删除当前的预约
def delete_seat():
    resv_info = get_resv_info()
    print(resv_info)
    if resv_info is not None:
        _resv_id = resv_info['id']
        delete_seat_with_id(_resv_id)


# 查询空座(指定阅览室）
def check_empty(startime, endtime, room_id='100457211'):
    _date = time.strftime("%Y-%m-%d", time.localtime())
    _url = get_room_status_url.format(room_id, _date, startime, endtime)  # 拼接地址
    result = {}

    response = evil_session.get(_url)
    data = json.loads(response.text)

    if data['ret'] == 1:
        seats = data['data']
        for seat in seats:
            if len(seat['ts']) == 0:
                result['msg'] = "找到空座:" + seat['devName']
                result['seat_id'] = str(seat['id']).split('_')[0]
                result['time'] = [startime, endtime]
                return result


# 查询空座（不限阅览室）
def get_empty(start_time, end_time):
    room_ids = ['100457211']
    for room_id in room_ids:
        print(check_empty(start_time, end_time, room_id)['msg'])
        return check_empty(start_time, end_time, room_id)


if __name__ == '__main__':
    pass


