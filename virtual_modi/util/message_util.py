
import json

from base64 import b64encode, b64decode


class MessageHandler:

    def __init__(self, modi_version=1):
        self.message_handler = {
            1: JsonMessageHandler,
            2: SwufMessageHandler,
        }.get(modi_version)

    def parse_modi_message(
        self, cmd, sid, did,
        byte_data=(None, None, None, None, None, None, None, None)
    ):
        return \
            self.message_handler.parse_modi_message(cmd, sid, did, byte_data)

    def unparse_modi_message(self, modi_message):
        return self.message_handler.unparse_modi_message(modi_message)

    @staticmethod
    def unpack_data(data, structure=(1, 1, 1, 1, 1, 1, 1, 1)):
        data = bytearray(b64decode(data.encode('utf8')))
        idx = 0
        result = []
        for size in structure:
            result.append(
                int.from_bytes(data[idx:idx + size], byteorder='little')
            )
            idx += size
        return result


class JsonMessageHandler:

    @staticmethod
    def parse_modi_message(
        cmd, sid, did,
        byte_data=(None, None, None, None, None, None, None, None)
    ):
        message = dict()
        message['c'] = cmd
        message['s'] = sid
        message['d'] = did
        message['b'] = JsonMessageHandler.encode_bytes(byte_data)
        message['l'] = len(byte_data)
        return json.dumps(message)

    @staticmethod
    def unparse_modi_message(modi_message):
        cmd = modi_message['c']
        sid = modi_message['s']
        did = modi_message['d']
        data = modi_message['b']
        dlc = modi_message['l']
        return cmd, sid, did, data, dlc

    #
    # Helper functions are defined below
    #
    @staticmethod
    def encode_bytes(byte_data):
        idx = 0
        data = bytearray(len(byte_data))
        while idx < len(byte_data):
            if not byte_data[idx]:
                idx += 1
            elif byte_data[idx] > 256:
                length = JsonMessageHandler.extract_length(idx, byte_data)
                data[idx: idx + length] = int.to_bytes(
                    byte_data[idx],
                    byteorder='little', length=length, signed=True
                )
                idx += length
            elif byte_data[idx] < 0:
                data[idx: idx + 4] = int.to_bytes(
                    int(byte_data[idx]),
                    byteorder='little', length=4, signed=True
                )
                idx += 4
            elif byte_data[idx] < 256:
                data[idx] = int(byte_data[idx])
                idx += 1
        return b64encode(bytes(data)).decode('utf8')

    @staticmethod
    def extract_length(begin, src):
        length = 1
        for i in range(begin + 1, len(src)):
            if not src[i]:
                length += 1
            else:
                break
        return length


class SwufMessageHandler:

    @staticmethod
    def parse_modi_message(
        cmd, sid, did,
        byte_data=(None, None, None, None, None, None, None, None)
    ):

        # Encode data section (sid: bytes, did: bytes, data: byte_array)
        sid_bytes = int.to_bytes(
            sid, byteorder='little', length=2, signed=False
        )
        did_bytes = int.to_bytes(
            did, byteorder='little', length=2, signed=False
        )
        data_bytes = bytes([b for b in byte_data if b])

        # Concat sid, did and data
        data_section = sid_bytes + did_bytes + data_bytes

        # Encode data_section
        data_section_encoded = SwufMessageHandler.encode_swuf(
            data_section
        )

        # Calculate CRC32 on the encoded data section
        crc32_value = SwufMessageHandler.calc_crc32_complete(
            data_section_encoded
        )

        # Encode CRC section
        #print('crc val:', crc32_value)
        #print('crc val:', int.to_bytes(crc32_value, byteorder='little', signed=False))
        crc_section = int.to_bytes(
            crc32_value, byteorder='little', length=4, signed=False
        )
        crc_section_encoded = SwufMessageHandler.encode_swuf(
            crc_section
        )

        # Init header section
        header_section = bytearray(4)
        header_section[0] = 0xAA
        header_section[1] = len(data_section_encoded)
        header_section[2] = len(crc_section_encoded)
        header_section[3] = cmd

        return header_section + data_section_encoded + crc_section_encoded

    @staticmethod
    def unparse_modi_message(modi_message):
        modi_message_decoded = \
            SwufMessageHandler.decode_swuf(modi_message)
        dlc = modi_message_decoded[1]
        cmd = modi_message_decoded[3]
        sid = int.from_bytes(modi_message_decoded[4:6], 'little')
        did = int.from_bytes(modi_message_decoded[6:8], 'little')
        data = int.from_bytes(modi_message_decoded[8:8 + dlc], 'little')
        return cmd, sid, did, data, dlc

    #
    # Helper functions are defined below
    #
    @staticmethod
    def encode_swuf(swuf):
        return swuf.replace(b'\xAA', b'\xDB\xDC').replace(b'\xDB', b'\xDB\xDD')

    @staticmethod
    def decode_swuf(swuf):
        return swuf.replace(b'\xDB\xDC', b'\xAA').replace(b'\xDB\xDD', b'\xDB')

    @staticmethod
    def validate_swuf_message(swuf_message, clc, dlc):
        """
        Each raw (i.e. encoded) SWUF message must be validated with CRC32,
        the steps for validation consist of three steps as given below.
        """

        # Step 1. Decode CRC section of the raw SWUF message
        crc_section = swuf_message[-clc:]
        crc_section_decoded = \
            SwufMessageHandler.decode_swuf(crc_section)
        crc_given = int.from_bytes(crc_section_decoded, 'little')

        # Step 2. Calculate CRC32 of the encoded data section
        data_section_encoded = swuf_message[4:4+dlc]
        crc_obtained = SwufMessageHandler.calc_crc32_complete(
            data_section_encoded
        )

        # Step 3. Compare CRC given and obtained, check if they are equal
        return crc_given == crc_obtained

    @staticmethod
    def calc_crc32(data, crc):
        crc ^= int.from_bytes(data, 'little')
        for _ in range(32):
            if crc & (1 << 31) != 0:
                crc = (crc << 1) ^ 0x4C11DB7
            else:
                crc <<= 1
            crc &= 0xFFFFFFFF
        return crc

    @staticmethod
    def calc_crc32_complete(data):
        checksum = 0
        for i in range(0, len(data), 4):
            curr_data = data[i:i + 4]

            # If curr_data_section is not 32 bits, augment it with zeros
            while len(curr_data) < 4:
                curr_data += 0
            checksum = SwufMessageHandler.calc_crc32(curr_data, checksum)
        return checksum
