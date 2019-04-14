import util
import time,datetime
import sched
import schedule

s = sched.scheduler(time.time, time.sleep)


def job():
    pass


def run():
    print("开始执行定时抢座")
    schedule.every().day.at("6:30").to("6:40").do(job)


if __name__ == '__main__':
    pass
