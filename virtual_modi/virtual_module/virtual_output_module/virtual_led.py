
from virtual_modi.virtual_module.virtual_module import VirtualModule

from virtual_modi.util.message_util import decode_message
from virtual_modi.util.message_util import unpack_data


class VirtualLed(VirtualModule):

    RED = 2
    GREEN = 3
    BLUE = 4

    def __init__(self):
        super(VirtualLed, self).__init__()
        self.type = 'led'
        self.uuid = self.generate_uuid(0x4020)

        self.rgb = 0, 0, 0

        self.attach()

    def process_set_property_message(self, message):
        cmd, sid, did, data, dlc = decode_message(message)
        colors = bytes(unpack_data(data))
        red = int.from_bytes(colors[0:2], byteorder='little')
        green = int.from_bytes(colors[2:4], byteorder='little')
        blue = int.from_bytes(colors[4:6], byteorder='little')
        self.rgb = red, green, blue

    def run(self):
        r, g, b = self.rgb
        self.send_property_message(self.RED, r)
        self.send_property_message(self.GREEN, g)
        self.send_property_message(self.BLUE, b)
