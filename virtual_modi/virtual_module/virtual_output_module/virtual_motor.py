
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualMotor(VirtualModule):

    # Get Property
    UPPER_SPEED = 5
    UPPER_ANGLE = 6
    LOWER_SPEED = 13
    LOWER_ANGLE = 14

    def __init__(self, message_handler):
        super(VirtualMotor, self).__init__(message_handler)
        self.type = 'led'
        self.uuid = self.generate_uuid(0x4010)
        self.speed = 0, 0
        self.angle = 0, 0

        self.attach()

    def process_set_property_message(self, message):
        cmd, sid, did, data, dlc = \
            self.message_handler.compose_modi_message(message)
        motor_property = bytes(self.message_handler.unpack_data(data))
        which_motor = int.from_bytes(motor_property[0:2], byteorder='little')
        motor_mode = int.from_bytes(motor_property[2:4], byteorder='little')
        motor_value = int.from_bytes(motor_property[4:6], byteorder='little')

        if motor_mode == 1:
            if not which_motor:
                self.speed = motor_value, 0
            else:
                self.speed = 0, motor_value
        elif motor_mode == 2:
            if not which_motor:
                self.angle = motor_value, 0
            else:
                self.angle = 0, motor_value

    def run(self):
        upper_speed, lower_speed = self.speed
        upper_angle, lower_angle = self.angle
        self.send_property_message(self.UPPER_SPEED, upper_speed)
        self.send_property_message(self.UPPER_ANGLE, upper_angle)
        self.send_property_message(self.LOWER_SPEED, lower_speed)
        self.send_property_message(self.LOWER_ANGLE, lower_angle)
