
from random import randint
from abc import ABC
from abc import abstractmethod

from virtual_modi.util.message_util import parse_message
from virtual_modi.util.message_util import decode_message


class VirtualModule(ABC):
    def __init__(self):
        # List static info
        self.uuid = None
        self.type = None
        self.stm32_version = '1.0.0'

        # List dynamic info
        self.topology = {'r': 0, 't': 0, 'l': 0, 'b': 0}
        self.attached = True

        # Messages to send to the local machine (i.e. PC)
        self.messages_to_send = []

    @property
    def id(self):
        return self.uuid % 0xFFF

    def __str__(self):
        return f"{self.__class__.__name__} ({self.id})"

    @abstractmethod
    def run(self):
        """ 
        While a module is alive, this `run` function defines what messages 
        should be generated from the module.
        """
        pass

    def attach(self):
        self.send_assignment_message()
        self.send_topology_message()

    def process_received_message(self, message):
        cmd, *_ = decode_message(message)

        if cmd == 4:
            self.process_set_property_message(message)
            return

        # If cmd is not module specific
        process_message = {
            7: self.send_topology_message,
            8: self.send_assignment_message,
        }.get(cmd, lambda _: None)
        process_message()

    def process_set_property_message(self, message):
        pass

    @staticmethod
    def generate_uuid(module_type_prefix):
        return module_type_prefix << 32 | randint(1, 0xFFFFFFFF)

    def send_health_message(self):
        cpu_rate = randint(0, 100)
        bus_rate = randint(0, 100)
        mem_rate = randint(0, 100)
        battery_voltage = 0
        module_state = 2

        health_message = parse_message(
            0, self.id, 0,
            byte_data=(
                cpu_rate, bus_rate, mem_rate, battery_voltage, module_state
            )
        )
        self.messages_to_send.append(health_message)

    def send_assignment_message(self):
        stm32_version_digits = [int(d) for d in self.stm32_version.split('.')]
        stm32_version = (
                stm32_version_digits[0] << 13
                | stm32_version_digits[1] << 8
                | stm32_version_digits[2]
        )
        module_uuid = self.uuid.to_bytes(6, 'little')
        stm32_version = stm32_version.to_bytes(2, 'little')
        assignment_message = parse_message(
            5, self.id, 4095, byte_data=(module_uuid + stm32_version)
        )
        print(assignment_message)
        self.messages_to_send.append(assignment_message)

    def send_topology_message(self):
        topology_data = bytearray(8)
        for i, (_, module_id) in enumerate(self.topology.items()):
            curr_module_id = module_id.to_bytes(2, 'little')
            topology_data[i*2] = curr_module_id[0]
            topology_data[i*2+1] = curr_module_id[1]
        topology_message = parse_message(
            7, self.id, 0, byte_data=topology_data
        )
        self.messages_to_send.append(topology_message)

    def send_property_message(self, property_number, property_value):
        property_value_in_bytes = property_value.to_bytes(8, 'little')
        property_message = parse_message(
            31, self.id, property_number, byte_data=property_value_in_bytes
        )
        self.messages_to_send.append(property_message)
