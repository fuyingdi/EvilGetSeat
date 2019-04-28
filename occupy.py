"""
这个是为公众号服务的，旨在一条指令完成找座，占座，续约一系列功能
"""

from util import occupy,login,check_empty
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
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