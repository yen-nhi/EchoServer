import json
import socket
import threading
import time

from server.basic_echo_server import BasicEchoServer
from settings import SERVER_ADDR, METRIC_SERVER


class SocketWithLockThread(BasicEchoServer):
    def __init__(self):
        self.no_of_conns = 0
        self.no_of_req = 0
        self.size_ten_reqs = 0
        self.size_hundred_reqs = 0
        self.size_big_reqs = 0
        self.lock = threading.Lock()

    def create_data_socket(self):
        try:
            data_socket = self.create_socket(*SERVER_ADDR)
            self.listen_socket(data_socket, False)
        except KeyboardInterrupt as e:
            data_socket.close()


    def create_metric_socket(self):
        try:
            metric_socket = self.create_socket(*METRIC_SERVER)
            self.listen_socket(metric_socket, True)
        except KeyboardInterrupt as e:
            metric_socket.close()


    def listen_socket(self, s, metric=False):
        """
        Create new thread to handle new connection => each connection run on a new thread
        :param s: socket
        :param s: bool
        :return:
        """
        try:
            while True:
                conn, addr = s.accept()
                print(f'Listening from {addr}')

                if metric:
                    threading.Thread(target=self.get_metrics, args=(conn,)).start()
                else:
                    self.lock.acquire()
                    self.no_of_conns += 1
                    self.lock.release()
                    threading.Thread(target=self.read_data_from_socket, args=(conn,)).start()
        except KeyboardInterrupt:
            s.close()

    def read_data_from_socket(self, conn):
        """
        Read line from socket
        :return:
        """
        while not conn._closed:
            data = conn.recv(1024)
            if not data:
                conn.close()
            else:
                self.update_metric(len(data.decode('ascii')) - 2)
                conn.sendall(data)

    def update_metric(self, size):
        lock = threading.Lock()
        lock.acquire()
        self.no_of_req += 1
        if size < 10:
            self.size_ten_reqs += 1
        elif size >= 10 and size < 100:
            self.size_hundred_reqs += 1
        else:
            self.size_big_reqs += 1
        lock.release()

    def get_metrics(self, conn):
        """
        :param s: socket object
        :param server: Echo server object
        :return:
        """
        while not conn._closed:
            data = conn.recv(1024)
            if data.decode('ascii').strip() == 'metric':
                self.lock.acquire()
                payload = {
                    'total_connections': self.no_of_conns,
                    'total_requests': self.no_of_req,
                    'number_of_requests_size_less_than_10': self.size_ten_reqs,
                    'number_of_requests_size_from_10_to_less_than_100': self.size_hundred_reqs,
                    'number_of_requests_size_from_100': self.size_big_reqs
                }
                self.lock.release()
                conn.sendall(json.dumps(payload).encode('ascii'))
            else:
                conn.sendall(b'Wrong request\n')
            if not data:
                conn.close()

    def run_socket(self):
        threading.Thread(target=self.create_data_socket).start()
        threading.Thread(target=self.create_metric_socket).start()




if __name__ == '__main__':
    SocketWithLockThread().run_socket()


