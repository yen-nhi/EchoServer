import subprocess
import sys
import socket
import threading
import time
import unittest
from typing import List, Tuple

from server.utils import CustomThread


class Server(object):
    """
    A context manager for testing the echo server
    """
    def __init__(self, file_name: str):
        self.file_name = file_name
    def __enter__(self):
        self.process = subprocess.Popen([sys.executable, self.file_name])
        time.sleep(0.1)
        return self
    def __exit__(self, type, value, traceback):
        self.process.kill()
        self.process.wait()


def test_single_client_connection(addr: Tuple[str, int], data: bin, time_sleep: int = 0):
    """
    To mock a client connect to echo server
    :param addr: tuple(host, port)
    :param data: data in binary type
    :return: data from server response
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(addr)
        client.sendall(data)
        return client.recv(1024)



def test_multi_client_connection(addr: Tuple[str, int], data: List[bin], number_of_clients: int = 1):
    responses = []
    for i in range(number_of_clients):
        thread = CustomThread(target=test_single_client_connection, args=(addr, data[i], 1))
        thread.start()
        response = thread.join()
        responses.append(response)
    return responses




