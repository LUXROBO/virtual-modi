
import json


def decode_message(message):
    msg = json.loads(message)
    cmd = msg['c']
    sid = msg['s']
    did = msg['d']
    data = msg['b']
    dlc = msg['l']
    return cmd, sid, did, data, dlc
