import time

from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Process


def fn1(sl):
    while True:
        print(sl.buf())
        time.sleep(1)

def fn2(sl):
    while True:
        sl[0] += 1
        sl[1] += 2
        time.sleep(1)

if __name__ == '__main__':  

    smm = SharedMemoryManager()
    smm.start()
    sl = smm.ShareableList([123, 456])

    p1 = Process(target=fn1, args=(sl,))
    p2 = Process(target=fn2, args=(sl,))
    
    p1.start()
    p2.start()
    
    time.sleep(5)
    
    p1.join()
    p2.join()

    smm.shutdown()