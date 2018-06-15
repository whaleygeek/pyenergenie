# Basic EV1527/RT1527/FP1527 learning code style encoder
# 20bit address and 4bit cmd
# Various remotes seem to use different combinations for on/off - I only have examples from one manufacturer
# https://www.sunrom.com/get/206000
# http://www.electrodragon.com/w/images/7/7b/RT1527E.pdf
# http://www.sc-tech.cn/en/SCL1527.pdf
# TODO: Tri-state
# More work may be required to interoperate with other remotes

PREAMBLE = [0x80, 0x00, 0x00, 0x00]

DEFAULT_ADDR = 0x6CC9D0

def ashex(payload): # -> str with hexascii bytes
    line = ""
    for b in payload:
        line += str(hex(b)) + " "
    return line

def encode_send_msg(cmd, house_address=None, repeat=3): # -> list of numbers
    """Build a message to turn a switch on or off"""
    ##print("build: state:%s, device:%d, house:%s" % (str(state), device_address, str(house_address)))

    if house_address == None:
        house_address = DEFAULT_ADDR

    payload = [] + PREAMBLE
    send = encode_bits((house_address | cmd), 24)

    payload += send * repeat

    ##print("encoded as:%s" % ashex(payload))
    return payload

def encode_bytes(data): # -> list of numbers
    """Turn a list of bytes into a modulated pattern equivalent"""
    ##print("modulate_bytes: %s" % ashex(data))
    payload = []
    for b in data:
        payload += encode_bits(b, 8)
    ##print("  returns: %s" % ashex(payload))
    return payload


ENCODER = [0x88, 0x8E, 0xE8, 0xEE]

def encode_bits(data, number): # -> list of numbers
    """Turn bits into n bytes of modulation patterns"""
    # 0000 00BA gets encoded as:
    # 128 64 32 16  8  4  2  1
    #   1  B  B  0  1  A  A  0
    # i.e. a 0 is a short pulse, a 1 is a long pulse
    ##print("modulate_bits %s (%s)" % (ashex(data), str(number)))

    shift = number-2
    encoded = []
    for i in range(int(number/2)):
        bits = (data >> shift) & 0x03
        ##print("    shift %d bits %d" % (shift, bits))
        encoded.append(ENCODER[bits])
        shift -= 2
    ##print("  returns:%s" % ashex(encoded))
    return encoded


def decode_switch_message(bytes): # -> (house_address, device_index, state)
    pass #TODO

def decode_command(bytes): #-> (device_index, state)
    pass #TODO


def decode_bytes(bytes): # -> list of numbers, decoded bytes
    pass #TODO


def decode_bits(bits, number): # -> list of bytes, decoded bits
    pass #TODO



# END
