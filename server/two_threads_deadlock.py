import threading
import time


# TODO: write example for deadlock


lock_1 = threading.Lock()
lock_2 = threading.Lock()

def func_1():
    for i in range(100000):
        with lock_1:
            with lock_2:
                print("f1  succsess ",i)
def func_2():
    for i in range(100000):
        with lock_2:
            with lock_1:
                print("f2  succsess ",i)

def two_thread_lock_blocking():
    thread_1 = threading.Thread(target=func_1)
    thread_2 = threading.Thread(target=func_2)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()



if __name__ == '__main__':
    two_thread_lock_blocking()
    print('DONE')