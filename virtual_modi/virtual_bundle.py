
import os
import time
import threading as th

from importlib.util import find_spec

from virtual_modi.util.message_util import decode_message


class VirtualBundle:
    """
    A virtual interface between a local machine and the virtual network module
    """

    def __init__(self, modules=None, gui=False, verbose=False):
        # Init flag to check if the program is running on GUI
        self.gui = gui

        # Init flag decide whether to suppress messages or not
        self.verbose = verbose

        # Create virtual modules have been initialized
        self.attached_virtual_modules = list()

        # Messages to be sent out to the local machine (i.e. PC)
        self.external_messages = list()

        # Start module initialization by creating a network module at first
        vnetwork = self.create_new_module('network')

        # If no modules are specified, create network, button and led modules
        if not gui and not modules:
            vbutton = self.create_new_module('button')
            vled = self.create_new_module('led')

            vnetwork.attach_module('r', vbutton)
            vbutton.attach_module('b', vled)
        else:
            for module_name in modules:
                self.create_new_module(module_name.lower())

        self.t = None

    def open(self):
        # Start all threads
        self.t = th.Thread(target=self.collect_module_messages, args=[0.1], daemon=True)
        self.t.start()

    def close(self):
        # Kill all threads

        # TODO: Find a proper way to kill running threads
        del self.t
        os._exit(0)

    def send(self):
        msg_to_send = ''.join(self.external_messages)
        self.external_messages = []
        return msg_to_send.encode()

    def recv(self, msg):
        _, _, did, _, _ = decode_message(msg)
        if did == 4095:
            for current_module in self.attached_virtual_modules:
                current_module.process_received_message(msg)
        else:
            for current_module in self.attached_virtual_modules:
                curr_module_id = current_module.id
                if curr_module_id == did:
                    current_module.process_received_message(msg)
                    break

    #
    # Helper functions below
    #
    def create_new_module(self, module_type):
        module_template = self.create_module_from_type(module_type)
        module_instance = module_template()
        self.attached_virtual_modules.append(module_instance)
        if self.verbose:
            print(f"{str(module_instance)} has been created!")
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

    def collect_module_messages(self, delay):
        while True:
            # Collect messages generated from each module
            for current_module in self.attached_virtual_modules:
                # Generate module message
                current_module.send_health_message()
                current_module.run()

                # Collect the generated module message
                self.external_messages.extend(current_module.messages_to_send)
                current_module.messages_to_send.clear()
            time.sleep(delay)
