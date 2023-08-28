import unittest

from settings import SERVER_ADDR
from tests.common_test import Server, test_single_client_connection, test_multi_client_connection


MAIN_FILE = "../server/single_thread_nonblocking.py"


class TestSingleThreadNonBlocking(unittest.TestCase):

    def test_single_thread_non_blocking_loop_single_client(self):
        with Server(MAIN_FILE):
            data_test = b'test_case_1'
            response = test_single_client_connection(SERVER_ADDR, data_test)
            assert response == data_test

    def test_single_thread_non_blocking_loop_multi_connection(self):
        with Server(MAIN_FILE):
            data_set = [b'test_1', b'test_2', b'test_3']
            reponses = test_multi_client_connection(SERVER_ADDR, data_set, 3)
            assert reponses == data_set