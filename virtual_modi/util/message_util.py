
import json
import struct

from base64 import b64encode, b64decode


def parse_message(cmd, sid, did,
                  byte_data=(None, None, None, None, None, None, None, None)):
    message = dict()
    message['c'] = cmd
    message['s'] = sid
    message['d'] = did
    message['b'] = __encode_bytes(byte_data)
    message['l'] = len(byte_data)
    return json.dumps(message, separators=(",", ":"))


def decode_message(message):
    msg = json.loads(message)
    cmd = msg['c']
    sid = msg['s']
    did = msg['d']
    data = msg['b']
    dlc = msg['l']
    return cmd, sid, did, data, dlc


def decode_data(data: str) -> float:
    return round(struct.unpack('f', bytes(unpack_data(data)[:4]))[0], 2)


def unpack_data(data, structure=(1, 1, 1, 1, 1, 1, 1, 1)):
    data = bytearray(b64decode(data.encode('utf8')))
    idx = 0
    result = []
    for size in structure:
        result.append(int.from_bytes(data[idx:idx + size], byteorder='little'))
        idx += size
    return result


#
# Helper functions
#
def __encode_bytes(byte_data):
    idx = 0
    data = bytearray(len(byte_data))
    while idx < len(byte_data):
        if not byte_data[idx]:
            idx += 1
        elif byte_data[idx] > 256:
            length = __extract_length(idx, byte_data)
            data[idx: idx + length] = int.to_bytes(
                byte_data[idx], byteorder='little', length=length, signed=True
            )
            idx += length
        elif byte_data[idx] < 0:
            data[idx: idx + 4] = int.to_bytes(
                int(byte_data[idx]), byteorder='little', length=4, signed=True
            )
            idx += 4
        elif byte_data[idx] < 256:
            data[idx] = int(byte_data[idx])
            idx += 1
    return b64encode(bytes(data)).decode('utf8')


def __extract_length(begin, src):
    length = 1
    for i in range(begin + 1, len(src)):
        if not src[i]:
            length += 1
        else:
            break
    return length
