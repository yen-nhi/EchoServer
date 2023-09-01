import unittest
import socket
import threading

from settings import SERVER_ADDR
from tests.common_test import Server, test_single_client_connection, test_multi_client_connection, \
    test_multi_client_connection_2

MAIN_FILE = "../server/multi_thread_blocking.py"



class TestMultiThreadingEchoServer(unittest.TestCase):

    def test_multithread_single_client(self):
        with Server(MAIN_FILE):
            data_test = b'test_case_1'
            response = test_single_client_connection(SERVER_ADDR, data_test)
            assert response == data_test

    def test_multithread_multi_connection(self):
        with Server(MAIN_FILE):
            data_set = [b'test_1', b'test_2', b'test_3']
            reponses = test_multi_client_connection_2(SERVER_ADDR, data_set, 3)
            assert reponses == data_set

