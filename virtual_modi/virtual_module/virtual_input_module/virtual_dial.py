
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualDial(VirtualModule):

    DEGREE = 2
    TURNSPEED = 3

    def __init__(self):
        super(VirtualDial, self).__init__()
        self.type = 'dial'
        self.uuid = self.generate_uuid(0x2040)

        self.degree = 0
        self.turnspeed = 0

        self.attached()

    def run(self):
        self.send_property_message(self.DEGREE, self.degree)
        self.send_property_message(self.TURNSPEED, self.turnspeed)
