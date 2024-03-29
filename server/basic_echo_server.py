import socket
from settings import SERVER_HOST, SERVER_PORT


class BasicEchoServer:

    def create_socket(self, host=SERVER_HOST, port=SERVER_PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        return s

    def read_from_socket(self, conn):
        """
        Read line from socket
        :return:
        """
        try:
            while not conn._closed:
                # print(conn)
                data = conn.recv(1024)
                if not data:
                    conn.close()
                else:
                    print(f'data received from {conn.getpeername()}: {data}')
                    conn.sendall(data)
        except KeyboardInterrupt:
            conn.close()

    def socket_run(self):
        try:
            s = self.create_socket()
            conn, addr = s.accept()
            print(f"Listening from {addr}")
            self.read_from_socket(conn)
        except KeyboardInterrupt:
            s.close()


