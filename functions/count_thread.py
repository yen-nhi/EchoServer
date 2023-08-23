import threading, time


TIMER = 300

def hanging(sleeping_time):
    time.sleep(sleeping_time)

def get_max_threads():
    try:
        counter = 1
        while True:
            threading.Thread(target=hanging, args=(TIMER,), daemon=True).start()
            counter += 1

    except Exception as err:
        print(f'REACH ERROR | {err}')
        print(f'MAX NUMBER OF THREADS ON THIS SERVER: {counter}')
