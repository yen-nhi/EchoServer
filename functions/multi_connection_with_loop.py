from collections import deque
from functions.basic_echo_server import BasicEchoServer


class SocketWithLoop(BasicEchoServer):

    def socket_run(self):
        """
        Use Non-blocking sockets to handle multi-connection sockets with looping
        :param s:
        """
        s = self.create_socket()
        s.setblocking(False)
        connections = deque()
        try:
            while True:
                try:
                    conn, addr = s.accept()
                    conn.setblocking(False)
                    connections.append(conn)
                    print(conn.getblocking())
                except BlockingIOError:
                    pass
                for i in range(len(connections)):
                    connection = connections.popleft()
                    try:
                        data = connection.recv(1024)
                        if data:
                            connections.append(connection)
                            print(data)
                            connection.sendall(data)
                    except BlockingIOError:
                        connections.append(connection)
                        pass
        except KeyboardInterrupt:
            for connection in connections:
                connection.close()
            s.close()







