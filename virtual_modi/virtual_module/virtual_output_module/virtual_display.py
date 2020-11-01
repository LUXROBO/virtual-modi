
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualDisplay(VirtualModule):

    def __init__(self, message_handler):
        super(VirtualDisplay, self).__init__(message_handler)
        self.type = 'display'
        self.uuid = self.generate_uuid(0x4000)

        self.text_buffer = []
        self.text = ''
        self.position = 0, 0

        self.attach()

    def process_set_property_message(self, message):
        cmd, sid, did, data, dlc = \
            self.message_handler.compose_modi_message(message)
        display_value = bytes(self.message_handler.unpack_data(data))
        if cmd == 17:
            text = [chr(t) for t in display_value]

            self.text_buffer.append(text)
            if text[-1] == '\0':
                self.text = ''.join(self.text_buffer)
                self.text_buffer.clear()
        elif cmd == 21:
            clear_status = int.from_bytes(
                display_value[0:2], byteorder='little'
            )
            if not clear_status:
                self.text = ''
            else:
                self.text_buffer.clear()

    def run(self):
        pass
