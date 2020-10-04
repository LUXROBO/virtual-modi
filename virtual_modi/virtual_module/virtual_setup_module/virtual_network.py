
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualNetwork(VirtualModule):

    def __init__(self):
        self.topology.pop("l") # network module cannot have the left neighbor
        self.esp32_verison = None
