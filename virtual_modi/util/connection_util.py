
import socket as s

from abc import ABC
from abc import abstractmethod


class Communicator(ABC):

    def __init__(self):
        self.conn = None

        #
        # Abstract Methods
        #
        @abstractmethod
        def open(self):
            pass

        @abstractmethod
        def close(self):
            pass

        @abstractmethod
        def send(self):
            pass

        @abstractmethod
        def recv(self):
            pass


class SerConn(Communicator):
    # TODO: Implement Serial Connection Task
    pass


class TcpConn(Communicator):

    def __init__(self):
        super().__init__()

    def open(self):
        serv_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        serv_host, serv_port = '127.0.0.1', 12345
        while True:
            try:
                serv_sock.bind((serv_host, serv_port))
            except OSError:
                print(
                    'PORT num is incremented!'
                )
                serv_port += 1
            else:
                break

        # Allow only one client
        serv_sock.listen(1)
        print('Be ready to accept a MODI software client')
        self.conn, addr = serv_sock.accept()
        print('A MODI software client is connected at', addr)
        return serv_host, serv_port

    def close(self):
        self.conn.close()

    def send(self, modi_message):
        return self.conn.sendall(modi_message)

    def recv(self):
        return self.recvall()

    def recvall(self):
        data = bytearray()
        while True:
            packet = self.conn.recv(1024)
            if not packet:
                break
            data.extend(packet)
        return data
