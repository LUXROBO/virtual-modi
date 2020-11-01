
from random import randint
from abc import ABC
from abc import abstractmethod


class VirtualModule(ABC):
    def __init__(self, message_handler):
        # List static info
        self.uuid = None
        self.type = None
        self.stm32_version = '1.0.0'

        # List dynamic info
        self.topology = {'r': 0, 't': 0, 'l': 0, 'b': 0}
        self.attached = True

        # Set modi message handler
        self.message_handler = message_handler

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

    def attach_module(self, direction, module):
        directions = ('r', 't', 'l', 'b')
        if direction and direction not in directions:
            raise ValueError("Not Supported Direction Type")

        # Attach the input module to self at random location
        if not direction:
            rand_dir_idx_max = len(directions) - 1
            rand_dir_idx = randint(0, rand_dir_idx_max)
            rand_dir = directions[rand_dir_idx]

            # All directions are occupied, try another method
            if all([v for k, v in self.topology.items()]):
                raise ValueError(
                    'All directions are occupied for current module'
                )

            while self.topology.get(rand_dir):
                rand_dir = directions[randint(0, rand_dir_idx_max)]
            direction = rand_dir

        # Attach input module and current module to the attached module
        self.topology[direction] = module
        opposite_direction_index = (
            (directions.index(direction) + 2) % len(directions)
        )
        opposite_direction = directions[opposite_direction_index]
        module.topology[opposite_direction] = self

        # Once attached, send required messages
        module.send_assignment_message()
        module.send_topology_message()

    def attach(self):
        self.send_assignment_message()
        self.send_topology_message()

    def process_received_message(self, message):
        cmd, *_ = self.message_handler.compose_modi_message(message)

        if cmd == 4:
            self.process_set_property_message(message)
            return

        # If cmd is not module specific
        process_message = {
            7: self.send_topology_message,
            8: self.send_assignment_message,
        }.get(cmd, lambda: None)
        process_message()

    def process_set_property_message(self, message):
        pass

    @staticmethod
    def generate_uuid(module_type_prefix):
        # TODO: Prohibit UUID with the last three digits of 000s for FFFs
        return module_type_prefix << 32 | randint(1, 0xFFFFFFFF)

    def send_health_message(self):
        cpu_rate = randint(0, 100)
        bus_rate = randint(0, 100)
        mem_rate = randint(0, 100)
        battery_voltage = 0
        module_state = 2

        health_message = self.message_handler.parse_modi_message(
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
        assignment_message = self.message_handler.parse_modi_message(
            5, self.id, 4095, byte_data=(module_uuid + stm32_version)
        )
        self.messages_to_send.append(assignment_message)

    def send_topology_message(self):
        topology_data = bytearray(b'\xFF')*8
        for i, direction in enumerate(('r', 't', 'l', 'b')):
            module = self.topology[direction]
            if not module:
                continue
            module_id = module.id
            curr_module_id = module_id.to_bytes(2, 'little')
            topology_data[i*2] = curr_module_id[0]
            topology_data[i*2+1] = curr_module_id[1]
        topology_message = self.message_handler.parse_modi_message(
            7, self.id, 0, byte_data=topology_data
        )
        self.messages_to_send.append(topology_message)

    def send_property_message(self, property_number, property_value):
        property_value_in_bytes = property_value.to_bytes(8, 'little')
        property_message = self.message_handler.parse_modi_message(
            31, self.id, property_number, byte_data=property_value_in_bytes
        )
        self.messages_to_send.append(property_message)
