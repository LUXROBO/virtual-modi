
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualNetwork(VirtualModule):

    def __init__(self, message_handler):
        super(VirtualNetwork, self).__init__(message_handler)
        self.type = 'network'
        self.uuid = self.generate_uuid(0x0000)

        # Network module specific
        self.esp32_version = '1.0.0'

        self.send_assignment_message()
        self.send_topology_message()

        self.attach()

    def run(self):
        pass
