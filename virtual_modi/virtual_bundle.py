
from importlib.util import find_spec

from virtual_modi.util.message_util import decode_message


class VirtualBundle:
    """
    A virtual interface between a local machine and the virtual network module
    """

    def __init__(self, modules=None):
        # Create virtual modules have been initialized
        self.attached_virtual_modules = []

        # Messages to be sent out to the local machine (i.e. PC)
        self.external_messages = []

        if not modules:
            # TODO: Randomly create modules of 1 network, 1 input, 1 output
            self.create_new_module('network')
            self.create_new_module('button')
            self.create_new_module('led')
        else:
            # TODO: if modules are specified, create them accordingly
            for module_name in modules:
                module_name.title()

    def open(self):
        # Start all threads
        pass

    def close(self):
        # Kill all threads
        pass

    def send(self):
        msg_to_send = b''.join(self.external_messages)
        self.external_messages.clear()
        return msg_to_send

    def recv(self, msg):
        _, _, did, _, _ = decode_message(msg)
        if did == 4095:
            for virtual_module in self.attached_virtual_modules:
                virtual_module.process_received_message(msg)
        else:
            for virtual_module in self.attached_virtual_modules:
                curr_module_id = virtual_module.id
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
