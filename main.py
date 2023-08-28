import threading
import time

from server.basic_echo_server import BasicEchoServer
from server.multithread_blocking_lock import Metrics, SocketWithLockThread
from server.single_thread_nonblocking import SocketWithLoop
from server.multi_thread_blocking import SocketWithThread
from server.single_thread_select import SocketWithSelect

echo_processes = {
    '1': BasicEchoServer,
    '2': SocketWithThread,
    '3': SocketWithLoop,
    '4': SocketWithSelect,
    '5': SocketWithLockThread
}


if __name__ == '__main__':
    process = echo_processes.get('Choose server: ')
    process().socket_run()





