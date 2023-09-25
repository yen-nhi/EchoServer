import threading

def func(num, lock_1, lock_2):
    for i in range(1000):
        with lock_1:
            with lock_2:
                print(f'THREAD {num}: success {i}')


def n_thread_deadlock(n):
    threads = []
    lock_1 = threading.Lock()
    head_lock = lock_1
    lock_2 = threading.Lock()
    for i in range(n):
        if i == n-1:
            lock_2 = head_lock
        thread = threading.Thread(target=func, args=(i, lock_1, lock_2))
        threads.append(thread)
        thread.start()
        lock_1 = lock_2
        lock_2 = threading.Lock()
    for t in threads:
        t.join()
    print('DONE')

if __name__ == '__main__':
    n_thread_deadlock(5)
    print('DONE')