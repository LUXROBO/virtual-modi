
import os
import threading as th

from importlib.util import find_spec

from virtual_modi.util.message_util import decode_message


class VirtualBundle:
    """
    A virtual interface between a local machine and the virtual network module
    """

    def __init__(self, modules=None):
        # Create virtual modules have been initialized
        self.attached_virtual_modules = list()

        # Messages to be sent out to the local machine (i.e. PC)
        self.external_messages = list()

        if not modules:
            # If no module is specified, create network, button and led modules
            self.create_new_module('network')
            self.create_new_module('button')
            self.create_new_module('led')

            # A dirty hack for initializing topology map for virutal modules
            vnetwork, vbutton, vled = (
                self.attached_virtual_modules[0], 
                self.attached_virtual_modules[1], 
                self.attached_virtual_modules[2],
            )
            vnetwork.topology['r'] = vbutton
            vbutton.topology['l'] = vnetwork
            vbutton.topology['b'] = vled
            vled.topology['t'] = vbutton
        else:
            for module_name in modules:
                self.create_new_module(module_name.lower())

        #self.t = None

    def open(self):
        # Start all threads
        #t = th.Thread(target=self.collect_module_messages, daemon=True)
        #t.start()
        pass

    def close(self):
        # Kill all threads
        #del self.t
        #os._exit(0)
        pass

    def send(self):
        self.collect_module_messages()

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
                    virtual_module.process(msg)
                    break

    #
    # Helper functions below
    #
    def create_new_module(self, module_type):
        module_template = self.create_module_from_type(module_type)
        module_instance = module_template()
        self.attached_virtual_modules.append(module_instance)
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
        module_module = module_module_template.loader.load_module()
        module_name = 'Virtual' + module_type[0].upper() + module_type[1:]
        return getattr(module_module, module_name)

    def collect_module_messages(self):
        # Collect messages generated from each module
        for current_module in self.attached_virtual_modules:
            # Generate module message
            current_module.send_health_message()
            current_module.run()

            # Collect the generated module message
            self.external_messages.extend(current_module.messages_to_send)
            current_module.messages_to_send.clear()
