import select

from functions.basic_echo_server import BasicEchoServer


class SocketWithSelect(BasicEchoServer):
    def select_socket(self, s):
        s.setblocking(False)
        socket_list = [s]
        while True:
            read_sockets, _, _ = select.select(socket_list, [], [])
            print('SELECT')
            for sock in read_sockets:
                if sock is s:
                    conn, addr = sock.accept()
                    print(f'Accepted from {addr}')
                    conn.setblocking(False)
                    socket_list.append(conn)
                else:
                    data = sock.recv(1024)
                    if data:
                        print(f'Recieved from {sock.getpeername()}: {data}')
                        sock.sendall(data)
                    else:
                        sock.close()
                        socket_list.remove(sock)




    def socket_run(self):
        try:
            s = self.create_socket()
            self.select_socket(s)
        except KeyboardInterrupt:
            s.close()

