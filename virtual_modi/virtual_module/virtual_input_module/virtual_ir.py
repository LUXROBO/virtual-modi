
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualIr(VirtualModule):

    PROXIMITY = 2

    def __init__(self, message_handler):
        super(VirtualIr, self).__init__(message_handler)
        self.type = 'ir'
        self.uuid = self.generate_uuid(0x2060)
        self.proximity = 0

        self.attach()

    def run(self):
        self.send_property_message(self.PROXIMITY, self.proximity)
