
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualUltrasonic(VirtualModule):

    DISTANCE = 2

    def __init__(self, message_handler):
        super(VirtualUltrasonic, self).__init__(message_handler)
        self.type = 'ultrasonic'
        self.uuid = self.generate_uuid(0x2050)

        self.distance = 0

        self.attach()

    def run(self):
        self.send_property_message(self.DISTANCE, self.distance)
