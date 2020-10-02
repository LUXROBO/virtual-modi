
from virtual_modi.utility.message_util import decode_message


class VirtualBundle:
    """
    A virtual interface between a local machine and the virtual network module
    """

    def __init__(self):
        self.external_messages = []  # messages to send to the machine

        self.attached_virtual_modules = []

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

    # TODO: Handle BROADCAST_ID
    def recv(self, msg):
        cid, sid, did, data, dlc = decode_message(msg)
        for virtual_module in self.attached_virtual_modules:
            curr_module_id = virtual_module.id
            if curr_module_id == did:
                virtual_module.process(msg)
                break
