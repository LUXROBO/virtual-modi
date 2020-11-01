
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

    def open(self):
        server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        HOST, PORT = '', 12345
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        self.conn, addr = server_socket.accept()
        print('A client is connected at', addr)

    def close(self):
        self.conn.close()

    def send(self, modi_message):
        return self.conn.send(modi_message)

    def recv(self):
        return self.conn.recv(1024)


class DirConn(Communicator):
    def __init__(self):
        super(DirConn, self).__init__()
        self.modi_messages = list()

    def open(self):
        pass

    def close(self):
        pass

    def send(self, modi_message):
        return modi_message

    def recv(self):
        temp = self.modi_messages[:]
        self.modi_messages = []
        return temp

    # A helper method for direct message recv, used for PyMODI integration
    def recv_raw(self, modi_message):
        self.modi_messages.append(modi_message)
