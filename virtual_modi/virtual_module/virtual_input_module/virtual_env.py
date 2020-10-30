
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualEnv(VirtualModule):

    BRIGHTNESS = 2
    RED = 3
    GREEN = 4
    BLUE = 5
    TEMPERATURE = 6
    HUMIDITY = 7

    def __init__(self, message_handler):
        super(VirtualEnv, self).__init__(message_handler)
        self.type = 'env'
        self.uuid = self.generate_uuid(0x2000)

        self.brightness = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.temperature = 0
        self.humidity = 0

        self.attach()

    def run(self):
        self.send_property_message(self.BRIGHTNESS, self.brightness)
        self.send_property_message(self.RED, self.red)
        self.send_property_message(self.GREEN, self.green)
        self.send_property_message(self.BLUE, self.blue)
        self.send_property_message(self.TEMPERATURE, self.temperature)
        self.send_property_message(self.HUMIDITY, self.humidity)
