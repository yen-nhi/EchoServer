import queue
import threading
from typing import Tuple

# from multiprocessing.pool import ThreadPool
from server.basic_echo_server import BasicEchoServer


#TODO: Using ThreadPool object made-by-me to implement threadpool echo server
class ThreadPool:
    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.channel = queue.Queue()

    def push_task(self, func, args: Tuple):
        self.channel.put(lambda: func(*args))

    def worker(self):
        while True:
            task = self.channel.get()
            task()

    def run(self):
        pool = [threading.Thread(target=self.worker) for _ in range(self.pool_size)]
        for thread in pool:
            thread.start()


class ThreadPoolServer3(BasicEchoServer):
    def __init__(self, pool_size):
        self.pool = ThreadPool(pool_size)
        self.sock = self.create_socket()

    def task(self, conn):
        while not conn._closed:
            data = conn.recv(1024)
            if data:
                conn.sendall(data)
            else:
                conn.close()

    def run_threadpool(self):
        try:
            self.pool.run()
            while True:
                conn, addr = self.sock.accept()
                self.pool.push_task(self.task, (conn,))
        except KeyboardInterrupt or Exception:
            self.sock.close()



#TODO: Simple way to implement threadpool echo server
class ThreadPoolServer2(BasicEchoServer):
    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.sock = self.create_socket()

    def worker(self):
        while True:
            conn, addr = self.sock.accept()
            print(f'ACCEPTED from {addr}')
            while not conn._closed:
                data = conn.recv(1024)
                if data:
                    conn.sendall(data)
                else:
                    conn.close()

    def run_threadpool(self):
        pool = [threading.Thread(target=self.worker) for _ in range(self.pool_size)]
        for thread in pool:
            thread.start()


#TODO: Using ThreadPool built-in python object to implement threadpool echo server
class ThreadPoolServer1(BasicEchoServer):

    def run_threadpool(self):
        try:
            s = self.create_socket()
            pool = ThreadPool(2)
            with pool:
                while True:
                    conn, addr = s.accept()
                    print(f'ACCEPTED {addr}')
                    print('Starting task ...')
                    pool.apply_async(self.read_from_socket, (conn,))
        except KeyboardInterrupt:
            s.close()


if __name__ == '__main__':
    ThreadPoolServer3(2).run_threadpool()


