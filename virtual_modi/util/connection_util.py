import time

from abc import ABC
from abc import abstractmethod

from queue import Queue
from threading import Thread

from websocket_server import WebsocketServer


class Communicator(ABC):

    def __init__(self):
        self.bus = None

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


class SocConn(Communicator):

    def __init__(self):
        super().__init__()
        DEFAULT_SOC_PORT = 8765
        self.host = ''
        self.port = DEFAULT_SOC_PORT
        self.bus = WebsocketServer(host=self.host, port=self.port)

        self.recv_q = Queue()
        self.send_q = Queue()
        self.close_event = False

    def open(self):
        Thread(target=self.__open, daemon=True).start()
        Thread(target=self.__send_handler, daemon=True).start()
        return self.host, self.port

    def close(self):
        self.bus.server_close()

    def recv(self):
        if self.recv_q.empty():
            return None
        modi_message = self.recv_q.get()
        return modi_message

    def send(self, modi_message):
        self.send_q.put(modi_message)

    #
    # Helper Methods
    #
    def __open(self):
        def new_client(client, server):
            server.send_message_to_all(
                f'Hey all, a new client:{client} has joined us'
            )

        def client_left(client, server):
            server.send_message_to_all(
                f'Hey all, a client:{client} has left us'
            )

        # Set callback functions
        self.bus.set_fn_new_client(new_client)
        self.bus.set_fn_message_received(self.__recv_handler)
        self.bus.set_fn_client_left(client_left)

        # Run the server forever
        self.bus.run_forever()

    def __recv_handler(self, client, server, message):
        self.recv_q.put(message)

    def __send_handler(self):
        while not self.close_event:
            if self.send_q.empty():
                time.sleep(0.001)
                continue
            try:
                message = self.send_q.get()
                self.bus.send_message_to_all(message)
            except Exception:
                self.close_event = True

