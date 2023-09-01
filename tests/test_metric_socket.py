import json
import socket
import threading
import time
import unittest
from settings import SERVER_ADDR, METRIC_SERVER
from tests.common_test import Server

MAIN_FILE = '../server/multithread_blocking_lock.py'

class TestMetricEchoServer(unittest.TestCase):

    def test_client_connection_for_metric_socket(self):
        with Server(MAIN_FILE) as s:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(METRIC_SERVER)
                client.sendall(b'test')
                self.assertEqual(b'Wrong request\n', client.recv(1024))

    def mock_client_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(SERVER_ADDR)
        # Each socket send 1000 requests size < 10, 1000 requests size < 100, 1000 requests size > 100
        for _ in range(1000):
            for i in range(3):
                data = 'abc' * pow(10, i)
                s.sendall(data.encode('ascii'))
                s.recv(1024)
        s.close()


    def test_get_metric(self):
        with Server(MAIN_FILE) as s:

            # Create client socket to call metric
            metric_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            metric_client.connect(METRIC_SERVER)

            # Create 10 threads clients sockets
            for _ in range(10):
                print('START NEW THREAD')
                new_thread = threading.Thread(target=self.mock_client_socket)
                new_thread.start()
                new_thread.join()

            # Call server for metric
            metric_client.sendall(b'metric')
            response = metric_client.recv(1024)

            # Test result
            result = json.loads(response.decode('ascii'))
            metric_client.close()

        # 10 threads * 3000 requests/thread
        print(f'---------METRIC-------- \n{result}')
        assert result['total_requests'] == 30000
        assert result['total_connections'] == 10
        assert result['number_of_requests_size_less_than_10'] == 10000
        assert result['number_of_requests_size_from_10_to_less_than_100'] == 10000
        assert result['number_of_requests_size_from_100'] == 10000
