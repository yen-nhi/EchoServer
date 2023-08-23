from functions.basic_echo_server import BasicEchoServer
from functions.multi_connection_with_loop import SocketWithLoop
from functions.multi_connection_with_threads import SocketWithThread
from functions.multiconnection_with_select import SocketWithSelect

echo_processes = {
    '1': BasicEchoServer,
    '2': SocketWithThread,
    '3': SocketWithLoop,
    '4': SocketWithSelect
}


if __name__ == '__main__':
    process = echo_processes.get(input())()
    process.socket_run()