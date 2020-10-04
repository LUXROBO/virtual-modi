
from random import randint
from abc import abstractmethod

from virtual_modi.utility.message_util import parse_message


class VirtualModule:
    def __init__(self):

        # static info
        self.id = None
        self.uuid = None
        self.type = None
        self.stm32_version = '1.0.0'

        # dynamic info
        self.topology = {'r': 0, 't': 0, 'l': 0, 'b': 0}

        # Once created (i.e. attached), send assignment, topology once
        # Then send out health and property messages continuously

    @abstractmethod
    def process_received_message(self, msg):
        # TODO: Handle modi commands (i.e. modi instructions) below
        # 7, 8, 9
        pass

    def create_health_message(self):
        cpu_rate = randint(0, 100)
        bus_rate = randint(0, 100)
        mem_rate = randint(0, 100)
        battery_voltage = 0
        module_state = 2

        # TODO: Handle `reserved` bytes?
        health_message = parse_message(
            0, self.id, 0,
            byte_data=(
                cpu_rate, bus_rate, mem_rate, battery_voltage, module_state
            )
        )
        return health_message

    def create_assignment_message(self):
        stm32_version_digits = [int(d) for d in self.stm32_version.split('.')]
        stm32_version = (
                stm32_version_digits[0] << 13
                | stm32_version_digits[1] << 8
                | stm32_version_digits[2]
        )
        module_uuid = self.uuid.to_bytes(6, 'little')
        stm32_version = stm32_version.to_bytes(2, 'little')
        assignment_message = parse_message(
            5, self.id, 4095, byte_data=(module_uuid, stm32_version)
        )
        return assignment_message

    def create_topology_message(self):
        topology_data = bytearray(8)
        for i, (_, module_id) in enumerate(self.topology.items()):
            curr_module_id = module_id.to_bytes(2, 'little')
            topology_data[i*2] = curr_module_id[0]
            topology_data[i*2+1] = curr_module_id[1]
        topology_message = parse_message(
            7, self.id, 0, byte_data=topology_data
        )
        return topology_message

    def create_property_message(self):
        property_value = self.create_property_value()
        property_message = parse_message(
            31, self.id, 0, byte_data=property_value
        )
        return property_message

    # Each module has different property defined, thus each module inherits it
    @abstractmethod
    def create_property_value(self):
        pass
