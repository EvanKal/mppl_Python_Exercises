from multiprocessing import Process, Lock
import datetime


def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()
    return i

def getDays():
    dayToRetrieveDraws = datetime.date.today().replace(day=1)
    allDaysToRetrieve=[]
    today = datetime.date.today()
    while today > dayToRetrieveDraws:
        allDaysToRetrieve.append(dayToRetrieveDraws)
        nextDay = dayToRetrieveDraws.day + 1
        dayToRetrieveDraws = dayToRetrieveDraws.replace(day=nextDay)

    print(allDaysToRetrieve)
    return allDaysToRetrieve

if __name__ == '__main__':
    lock = Lock()
    for day in getDays():
        p = Process(target=f, args=(lock, day))
        p.start()
        p.join()
