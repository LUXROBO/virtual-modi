
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualIr(VirtualModule):

    PROXIMITY = 2

    def __init__(self):
        super(VirtualIr, self).__init__()
        self.proximity = 0

    def run(self):
        self.send_health_message()

        self.send_property_message(self.PROXIMITY, self.proximity)