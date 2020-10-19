
from virtual_modi.virtual_module.virtual_module import VirtualModule

from virtual_modi.util.message_util import decode_message
from virtual_modi.util.message_util import unpack_data


class VirtualSpeaker(VirtualModule):

    FREQUENCY = 3
    VOLUME = 2

    def __init__(self):
        super(VirtualSpeaker, self).__init__()
        self.type = 'speaker'
        self.uuid = self.generate_uuid(0x4030)

        self.tune = 1318, 0

        self.attach()

    def process_set_property_message(self, message):
        cmd, sid, did, data, dlc = decode_message(message)
        tune = bytes(unpack_data(data))
        frequency = int.from_bytes(tune[0:2], byteorder='little')
        volume = int.from_bytes(tune[2:4], byteorder='little')
        self.tune = frequency, volume

    def run(self):
        frequency, volume = self.tune
        self.send_property_message(self.FREQUENCY, frequency)
        self.send_property_message(self.VOLUME, volume)
