
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualUltrasonic(VirtualModule):

    DISTANCE = 2

    def __init__(self):
        super(VirtualUltrasonic, self).__init__()
        self.distance = 0

    def run(self):
        self.send_health_message()

        self.send_property_message(self.DISTANCE, self.distance)