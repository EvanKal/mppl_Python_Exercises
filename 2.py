from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
import multiprocessing as mp

list1=[]

def f(l, i, s):  
    l.acquire()
    try:
        s.append(i)
        print(i)
    finally:
        l.release()


def initiate():
    global list1
    shared_list=[]
    if __name__ == '__main__':
        lock = Lock()
        manager = mp.Manager()
        shared_list = manager.list()

        for num in range(10):
            p = Process(target=f, args=(lock, num, shared_list))
            p.start()
            p.join()
    
    list1 =  shared_list
    
    print(list1)
       
initiate()
