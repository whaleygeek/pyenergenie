# encoder.py  27/03/2016  D.J.Whale
#
# payload encoder for use with OOK payloads

ALL_SOCKETS = 0

# The preamble is now stored in the payload,
# this is more predictable than using the radio sync feature
PREAMBLE = [0x80, 0x00, 0x00, 0x00]

# This generates a 20*4 bit address i.e. 10 bytes
# The number generated is always the same
# This is the random 'Energenie address prefix'
# The switch number is encoded in the payload
# 0000 00BA gets encoded as:
# 128 64 32 16  8  4  2  1
#   1  B  B  0  1  A  A  0
#payload = []
#for i in range(10):
#    j = i + 5
#    payload.append(8 + (j&1) * 6 + 128 + (j&2) * 48)
#dumpPayloadAsHex(payload)

#this is just a fixed address generator, from the C code
#payload = []
#for i in range(10):
#    j = i + 5
#    payload.append(8 + (j&1) * 6 + 128 + (j&2) * 48)
#dumpPayloadAsHex(payload)
# binary = 0110 1100 0110 1100 0110
# hex    = 6    C    6    C    6

DEFAULT_ADDR = 0x6C6C6

#                   5     6     7     8     9     10    11    12    13    14
#                   1(01) 1(10) 1(11) 0(00) 0(01) 0(10) 0(11) 1(00) 1(01) 1(10)
DEFAULT_ADDR_ENC = [0x8e, 0xe8, 0xee, 0x88, 0x8e, 0xe8, 0xee, 0x88, 0x8e, 0xe8]

# D0=high, D1=high, D2-high, D3=high (S1 on) sent as:(D0D1D2D3)
# 128 64 32 16  8  4  2  1        128 64 32 16  8  4  2  1
#   1  B  B  0  1  A  A  0          1  B  B  0  1  A  A  0
#   1  1  1  0  1  1  1  0          1  1  1  0  1  1  1  0

SW1_ON_ENC  = [0xEE, 0xEE] # 1111 sent as 1111

# D0=high, D1=high, D2=high, D3=low (S1 off)
# 128 64 32 16  8  4  2  1        128 64 32 16  8  4  2  1
#   1  B  B  0  1  A  A  0          1  B  B  0  1  A  A  0
#   1  1  1  0  1  1  1  0          1  1  1  0  1  0  0  0

SW1_OFF_ENC = [0xEE, 0xE8] # 1110 sent as 0111


def ashex(payload):
    line = ""
    for b in payload:
        line += str(hex(b)) + " "
    return line


def build_relay_msg(relayState=False):
    """Temporary test code to prove we can turn the relay on or off"""

    payload = PREAMBLE

    if relayState: # ON
        payload += SW1_ON_ENC

    else: # OFF
        payload += SW1_OFF_ENC

    return payload


def build_test_message(pattern):
    """build a test message for a D3D2D1D0 control patter"""
    payload = PREAMBLE + DEFAULT_ADDR_ENC
    pattern &= 0x0F
    control = encode_bits(pattern, 4)
    payload += control
    return payload


def build_switch_msg(state, device_address=ALL_SOCKETS, house_address=None):
    """Build a message to turn a switch on or off"""
    #print("build: state:%s, device:%d, house:%s" % (str(state), device_address, str(house_address)))

    if house_address == None:
        house_address = DEFAULT_ADDR

    payload = [] + PREAMBLE
    payload += encode_bits((house_address & 0x0F0000) >> 16, 4)
    payload += encode_bits((house_address & 0x00FF00) >> 8,  8)
    payload += encode_bits((house_address & 0x0000FF),       8)

    # Coded as per the (working) C code, as it is transmitted D0D1D2D3:
    # D 0123
    # b 3210
    #   0000 UNUSED         0
    #   0001 UNUSED         1
    #   0010 socket 4 off   2
    #   0011 socket 4 on    3
    #   0100 UNUSED         4
    #   0101 UNUSED         5
    #   0110 socket 2 off   6
    #   0111 socket 2 on    7
    #   1000 UNUSED         8
    #   1001 UNUSED         9
    #   1010 socket 3 off   A
    #   1011 socket 3 on    B
    #   1100 all off        C
    #   1101 all on         D
    #   1110 socket 1 off   E
    #   1111 socket 1 on    F

    if not state: # OFF
        bits = 0x00
    else: # ON
        bits = 0x01

    if device_address == ALL_SOCKETS:
        bits |= 0x0C # ALL
    elif device_address == 1:
        bits |= 0x0E
    elif device_address == 2:
        bits |= 0x06
    elif device_address == 3:
        bits |= 0x0A
    elif device_address == 4:
        bits |= 0x02
        
    payload += encode_bits(bits, 4)
    #print("encoded as:%s" % ashex(payload))
    return payload


def encode_bytes(data):
    """Turn a list of bytes into a modulated pattern equivalent"""
    #print("modulate_bytes: %s" % ashex(data))
    payload = []
    for b in data:
        payload += encode_bits(b, 8)
    #print("  returns: %s" % ashex(payload))
    return payload


ENCODER = [0x88, 0x8E, 0xE8, 0xEE]

def encode_bits(data, number):
    """Turn bits into n bytes of modulation patterns"""
    # 0000 00BA gets encoded as:
    # 128 64 32 16  8  4  2  1
    #   1  B  B  0  1  A  A  0
    # i.e. a 0 is a short pulse, a 1 is a long pulse
    #print("modulate_bits %s (%s)" % (ashex(data), str(number)))

    shift = number-2
    encoded = []
    for i in range(int(number/2)):
        bits = (data >> shift) & 0x03
        #print("    shift %d bits %d" % (shift, bits))
        encoded.append(ENCODER[bits])
        shift -= 2
    #print("  returns:%s" % ashex(encoded))
    return encoded


# END

