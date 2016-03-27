# test_modulator.py  27/03/2016  D.J.Whale
#
# Test the OOK modulator


def ashex(data):
    if type(data) == list:
        line = ""
        for b in data:
            line += str(hex(b)) + " "
        return line
    else:
        return str(hex(data))

ALL_SOCKETS = 0

def build_OOK_relay_msg(state, device_address=ALL_SOCKETS, house_address=None):
    """Temporary test code to prove we can turn the relay on or off"""
    #This code does not live in this module, it lives in an EnergenieLegacy codec module
    print("build: state:%s, device:%d, house:%s" % (str(state), device_address, str(house_address)))

    if house_address == None:
        #this is just a fixed address generator, from the C code
        #payload = []
        #for i in range(10):
        #    j = i + 5
        #    payload.append(8 + (j&1) * 6 + 128 + (j&2) * 48)
        #dumpPayloadAsHex(payload)
        # binary = 0110 1100 0110 1100 0110
        # hex    = 6    C    6    C    6
        house_address = 0x6C6C6

    payload  = modulate_bits((house_address & 0x0F0000) >> 16, 4)
    payload += modulate_bits((house_address & 0x00FF00) >> 8,  8)
    payload += modulate_bits((house_address & 0x0000FF),       8)

    # Turn switch request into a 4 bit switch command, and add to payload
    # D 3210
    #   0000 UNUSED
    #   0001 UNUSED
    #   0010 UNUSED
    #   0011 All off      (3)
    #   0100 socket 4 off (4)
    #   0101 socket 3 off (5)
    #   0110 socket 2 off (6)
    #   0111 socket 1 off (7)
    #   1000 UNUSED
    #   1101 UNUSED
    #   1110 UNUSED
    #   1011 All on       (3)
    #   1100 socket 4 on  (4)
    #   1101 socket 3 on  (5)
    #   1110 socket 2 on  (6)
    #   1111 socket 1 on  (7)

    if not state: # OFF
        bits = 0x00
    else: # ON
        bits = 0x08

    if device_address == ALL_SOCKETS:
        bits |= 0x03 # ALL
    else:
        bits += 7-((device_address-1) & 0x03)

    payload += modulate_bits(bits, 4)
    return payload


def modulate_bytes(data):
    """Turn a list of bytes into a modulated pattern equivalent"""
    #print("modulate_bytes: %s" % ashex(data))
    payload = []
    for b in data:
        payload += modulate_bits(b, 8)
    #print("  returns: %s" % ashex(payload))
    return payload


MODULATOR = [0x88, 0x8E, 0xE8, 0xEE]

def modulate_bits(data, number):
    """Turn bits into n bytes of modulation patterns"""
    # 0000 00BA gets encoded as:
    # 128 64 32 16  8  4  2  1
    #   1  B  B  0  1  A  A  0
    # i.e. a 0 is a short pulse, a 1 is a long pulse
    #print("modulate_bits %s (%s)" % (ashex(data), str(number)))

    shift = number-2
    modulated = []
    for i in range(number/2):
        bits = (data >> shift) & 0x03
        #print("    shift %d bits %d" % (shift, bits))
        modulated.append(MODULATOR[bits])
        shift -= 2
    #print("  returns:%s" % ashex(modulated))
    return modulated


#----- TEST APPLICATION -------------------------------------------------------

print("*" * 80)

ALL_ON   = build_OOK_relay_msg(True)
ALL_OFF  = build_OOK_relay_msg(False)

ONE_ON   = build_OOK_relay_msg(True, device_address=1)
ONE_OFF  = build_OOK_relay_msg(False, device_address=1)

TWO_ON   = build_OOK_relay_msg(True, device_address=2)
TWO_OFF  = build_OOK_relay_msg(False, device_address=2)

THREE_ON   = build_OOK_relay_msg(True, device_address=3)
THREE_OFF  = build_OOK_relay_msg(False, device_address=3)

FOUR_ON   = build_OOK_relay_msg(True, device_address=4)
FOUR_OFF  = build_OOK_relay_msg(False, device_address=4)

MYHOUSE_ALL_ON = build_OOK_relay_msg(True, house_address=0x12345)

tests = [ALL_ON, ALL_OFF, ONE_ON, ONE_OFF, TWO_ON, TWO_OFF, THREE_ON, THREE_OFF, FOUR_ON, FOUR_OFF, MYHOUSE_ALL_ON]

for t in tests:
    print(ashex(t))

# END

