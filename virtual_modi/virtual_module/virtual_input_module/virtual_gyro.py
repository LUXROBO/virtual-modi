
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualGyro(VirtualModule):

    ROLL = 2
    PITCH = 3
    YAW = 4
    ANGULAR_VEL_X = 5
    ANGULAR_VEL_Y = 6
    ANGULAR_VEL_Z = 7
    ACCELERATION_X = 8
    ACCELERATION_Y = 9
    ACCELERATION_Z = 10
    VIBRATION = 11

    def __init__(self, message_handler):
        super(VirtualGyro, self).__init__(message_handler)
        self.type = 'gyro'
        self.uuid = self.generate_uuid(0x2010)

        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.ang_vel_x = 0
        self.ang_vel_y = 0
        self.ang_vel_z = 0
        self.acc_x = 0
        self.acc_y = 0
        self.acc_z = 0
        self.vibration = 0

        self.attach()

    def run(self):
        self.send_property_message(self.ROLL, self.roll)
        self.send_property_message(self.PITCH, self.pitch)
        self.send_property_message(self.YAW, self.yaw)
        self.send_property_message(self.ANGULAR_VEL_X, self.ang_vel_x)
        self.send_property_message(self.ANGULAR_VEL_Y, self.ang_vel_y)
        self.send_property_message(self.ANGULAR_VEL_Z, self.ang_vel_z)
        self.send_property_message(self.ACCELERATION_X, self.acc_x)
        self.send_property_message(self.ACCELERATION_Y, self.acc_y)
        self.send_property_message(self.ACCELERATION_Z, self.acc_z)
        self.send_property_message(self.VIBRATION, self.vibration)
