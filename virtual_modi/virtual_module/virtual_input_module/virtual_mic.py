
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualMic(VirtualModule):

    VOLUME = 2
    FREQUENCY = 3

    def __init__(self):
        super(VirtualMic, self).__init__()
        self.volume = 0
        self.frequency = 0

    def run(self):
        self.send_health_message()

        self.send_property_message(self.VOLUME, self.volume)
        self.send_property_message(self.frequency, self.frequency)