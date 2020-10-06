
from importlib.util import find_spec

from virtual_modi.utility.message_util import decode_message


class VirtualBundle:
    """
    A virtual interface between a local machine and the virtual network module
    """

    def __init__(self, modules=None):
        if not modules:
            # TODO: Randomly create modules of 1 network, 1 input, 1 output
            pass
        else:
            # TODO: if modules are specified, create them accordingly
            for module_name in modules:
                module_name.title()

        # Create virtual modules have been initialized
        self.attached_virtual_modules = []

        # Messages to be sent out to the local machine (i.e. PC)
        self.external_messages = []

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

    def create_virtual_module(self, module_name):
        pass

    #
    # Helper functions below
    #
    @staticmethod
    def create_module_from_name(module_type):
        module_type = module_type[0].lower() + module_type[1:]
        module_name = module_type[0].upper() + module_type[1:]
        virtual_module_path = 'virtual_module.virtual'
        module_module = (
            find_spec(f'{virtual_module_path}.input_module.{module_type}')
            or find_spec(f'{virtual_module_path}.output_module.{module_type}')
            or find_spec(f'{virtual_module_path}.setup_module.{module_type}')
        )
        module_module = module_module.loader.load_module()
        return getattr(module_module, module_name)

    def create_new_module(self):
        vmodule_template = get_module_from_name(module_type)
        vmodule_instance = module_template(
            module_id, module_uuid, self._conn
        )
        vmodule_instance.version = module_version_info
        self.attached_vmodules.append(module_instance)
        print(f"{str(module_instance)} has been connected!")
        return module_instance