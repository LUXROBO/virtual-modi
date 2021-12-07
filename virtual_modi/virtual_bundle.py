
import time
import threading as th

from random import randint

from importlib.util import find_spec

from virtual_modi.util.message_util import MessageHandler
from virtual_modi.util.topology_util import TopologyManager
from virtual_modi.util.connection_util import SocConn, SerConn


class VirtualBundle:
    """
    A virtual modi bundle which forms an interface between a local machine and
    the virtual network module.
    """

    def __init__(
        self, conn_type='soc', modi_version=1, modules=None, verbose=False
    ):
        # Init connection type, it decides the communication method
        self.conn = {
            'soc': SocConn(), 'ser': SerConn(),
        }.get(conn_type)

        self.running = True
        self.verbose = verbose

        # The message handler for the virtual bundle, which imitates MODI1 or 2
        self.modi_message_handler = MessageHandler(modi_version=modi_version)

        # A list which will contain created virtual modules
        self.attached_virtual_modules = list()

        # Messages to be sent out to MODI client(s)
        self.messages_to_sendout = list()

        # Start module initialization by creating a network module at first
        vnetwork = self.create_new_module('network')

        self.topology_manager = TopologyManager(self.attached_virtual_modules)

        # If no module is specified, init button and led modules as the default
        if not modules:
            vbutton = self.create_new_module('button')
            vled = self.create_new_module('led')

            vnetwork.attach_module('r', vbutton)
            vbutton.attach_module('b', vled)

    def run(self):
        self.conn.open()
        while self.running:
            time.sleep(0.1)
        self.conn.close()

    def open(self):
        serv_host, serv_port = self.conn.open()
        print('serv_host: {}, serv_port: {}'.format(serv_host, serv_port))

        # Start all threads
        property_thread = th.Thread(
            target=self.collect_property_message, args=(0.1,), daemon=True
        )
        property_thread.start()
        #health_thread = th.Thread(
        #    target=self.collect_health_message, args=(1,), daemon=True
        #)
        #health_thread.start()

        # Start communication threads(i.e. send and recv threads)
        th.Thread(target=self.send, args=(0.1,), daemon=True).start()
        th.Thread(target=self.recv, args=(0.1,), daemon=True).start()

    def close(self):
        self.conn.close()

        # Terminate all running threads
        self.running = False

    def send(self, delay=0):
        while self.running:
            if not self.messages_to_sendout:
                time.sleep(delay)
                continue
            for message_to_sendout in self.messages_to_sendout:
                self.conn.send(message_to_sendout)
            self.messages_to_sendout = []

    def recv(self, delay=0):
        while self.running:
            time.sleep(delay)
            modi_message = self.conn.recv()
            if not modi_message:
                return
            _, _, did, *_ = self.modi_message_handler.unparse_modi_message(
                modi_message
            )
            if did == 0xFFF:
                for current_module in self.attached_virtual_modules:
                    current_module.process_received_message(modi_message)
                continue
            target_module = self.find_module_by_id(did)
            if not target_module:
                print('Cannot find a virtual module with id:', did)
                continue
            target_module.process_received_message(modi_message)

    def print_topology_graph(self):
        self.topology_manager.print_topology_graph()

    #
    # Helper functions below
    #
    def create_new_module(self, module_type):
        module_template = self.create_module_from_type(module_type)
        module_instance = module_template(self.modi_message_handler)
        self.attached_virtual_modules.append(module_instance)
        if self.verbose:
            print(f'{str(module_instance)} has been created!')
        return module_instance

    @staticmethod
    def create_module_from_type(module_type):
        module_type = module_type[0].lower() + module_type[1:]
        module_path = 'virtual_modi.virtual_module.virtual'
        module_module_template = (
            find_spec(f'{module_path}_input_module.virtual_{module_type}')
            or find_spec(f'{module_path}_output_module.virtual_{module_type}')
            or find_spec(f'{module_path}_setup_module.virtual_{module_type}')
        )
        module_module = module_module_template.loader.load_module(
            module_module_template.name
        )
        module_name = 'Virtual' + module_type[0].upper() + module_type[1:]
        return getattr(module_module, module_name)
    
    def find_module_by_id(self, module_id):
        for current_module in self.attached_virtual_modules:
            if current_module.id == module_id:
                return current_module

    def collect_property_message(self, delay):
        while self.running:
            time.sleep(delay)

            # Collect messages generated from each module
            for current_module in self.attached_virtual_modules:
                # Generate module message
                current_module.run()

                # Collect the generated module message
                self.messages_to_sendout.extend(
                    current_module.messages_to_send
                )
                current_module.messages_to_send.clear()

    #def collect_health_message(self, delay):
    #    while self.running:
    #        time.sleep(delay)
    #
    #        for current_module in self.attached_virtual_modules:
    #            current_module.send_health_message()
    #            self.messages_to_sendout.extend(current_module.messages_to_send)
    #            current_module.messages_to_send.clear()

