
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualNetwork(VirtualModule):

    def __init__(self):
        super(VirtualNetwork, self).__init__()
        self.type = 'network'
        self.uuid = self.generate_uuid(0x0000)

        # Network module specific
        self.topology.pop("l")
        self.esp32_version = '1.0.0'

        self.send_assignment_message()
        self.send_topology_message()

        self.attached()

    def run(self):
        pass
