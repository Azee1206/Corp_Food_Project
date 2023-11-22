import schedule
import datetime


def a():
    print("aaaa")


def a_once():
    a()
    return schedule.CancelJob


print(datetime.datetime.now())
schedule.every(1).minutes.do(a_once)

while True:
    schedule.run_pending()

