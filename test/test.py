import unittest
import socket

from functions.multi_connection_with_threads import SocketWithThread
import threading


class TestEchoServer(unittest.TestCase):

    def test_multithread(self):
        use_case = SocketWithThread()
        server_socket = use_case.create_socket()
        echo_server_thread = threading.Thread(target=use_case.multithread_connection, args=(server_socket,), daemon=True)
        echo_server_thread.start()

        responses = []
        client_sockets = []

        # Create clients connect to sever socket
        for i in ('first_socket', 'second_socket'):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 8000))
            addr = s.getsockname()
            data = str(i).encode('ascii')
            s.sendall(data)
            client_sockets.append(s)
            responses.append((addr, s.recv(1024).decode('ascii')))
        assert client_sockets[0]._closed is False and client_sockets[1]._closed is False
        assert responses[0][0] != responses[1][0]
        assert responses[0][1] != responses[1][1]

        for sock in client_sockets:
            sock.close()
        assert client_sockets[0]._closed is True and client_sockets[1]._closed is True

        server_socket.close()




