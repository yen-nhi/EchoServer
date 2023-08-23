import threading
from functions.basic_echo_server import BasicEchoServer


class SocketWithThread(BasicEchoServer):

    def multithread_connection(self, s):
        """
        Create new thread to handle new connection => each connection run on a new thread
        :param s:
        :return:
        """
        try:
            while True:
                conn, addr = s.accept()
                print(f'Listening from {addr}')
                threading.Thread(target=self.read_from_socket, args=(conn,)).start()
        except KeyboardInterrupt:
            s.close()

    def read_from_socket(self, conn):
        """
        Read line from socket
        :return:
        """
        while not conn._closed:
            print(conn)
            data = conn.recv(1024)
            if not data:
                conn.close()
            else:
                print(f'data received: {data}')
                conn.sendall(data)

    def socket_run(self):
        s = self.create_socket()
        self.multithread_connection(s)

