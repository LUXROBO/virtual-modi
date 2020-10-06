
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualNetwork(VirtualModule):

    def __init__(self):
        super(VirtualNetwork, self).__init__()
        self.type = 'network'

        # Network module specific
        self.topology.pop("l")
        self.esp32_version = '1.0.0'

    def run(self):
        self.send_health_message()
