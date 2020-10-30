
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualSpeaker(VirtualModule):

    FREQUENCY = 3
    VOLUME = 2

    def __init__(self, message_handler):
        super(VirtualSpeaker, self).__init__(message_handler)
        self.type = 'speaker'
        self.uuid = self.generate_uuid(0x4030)

        self.tune = 1318, 0

        self.attach()

    def process_set_property_message(self, message):
        cmd, sid, did, data, dlc = \
            self.message_handler.compose_modi_message(message)
        tune = bytes(self.message_handler.unpack_data(data))
        frequency = int.from_bytes(tune[0:2], byteorder='little')
        volume = int.from_bytes(tune[2:4], byteorder='little')
        self.tune = frequency, volume

    def run(self):
        frequency, volume = self.tune
        self.send_property_message(self.FREQUENCY, frequency)
        self.send_property_message(self.VOLUME, volume)
