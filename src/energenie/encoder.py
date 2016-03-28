# encoder.py  27/03/2016  D.J.Whale
#
# payload encoder for use with OOK payloads

ALL_SOCKETS = 0

def build_relay_msg(relayState=False):
    """Temporary test code to prove we can turn the relay on or off"""

    # This generates a 20*4 bit address i.e. 10 bytes
    # The number generated is always the same
    # Presumably this is the random 'Energenie address prefix'
    # The switch number is encoded in the payload

    # Looks like: 0000 00BA gets encoded as:
    # 128 64 32 16  8  4  2  1
    #   1  B  B  0  1  A  A  0

    #payload = []
    #for i in range(10):
    #    j = i + 5
    #    payload.append(8 + (j&1) * 6 + 128 + (j&2) * 48)
    #dumpPayloadAsHex(payload)
    #
    #          5     6     7     8     9     10    11    12    13    14
    #          1(01) 1(10) 1(11) 0(00) 0(01) 0(10) 0(11) 1(00) 1(01) 1(10)
    payload = [0x8e, 0xe8, 0xee, 0x88, 0x8e, 0xe8, 0xee, 0x88, 0x8e, 0xe8]

    #TODO: This is taken from the C code, it might be wrong
    #(the D bit order seems reversed compared to the pdf spec)
    if relayState: # ON
        # D0=high, D1=high, D2-high, D3=high (S1 on)
        # 128 64 32 16  8  4  2  1        128 64 32 16  8  4  2  1
        #   1  B  B  0  1  A  A  0          1  B  B  0  1  A  A  0
        #   1  1  1  0  1  1  1  0          1  1  1  0  1  1  1  0
        payload += [0xEE, 0xEE] # 1111

    else: # OFF
        # D0=high, D1=high, D2=high, D3=low (S1 off)
        # 128 64 32 16  8  4  2  1        128 64 32 16  8  4  2  1
        #   1  B  B  0  1  A  A  0          1  B  B  0  1  A  A  0
        #   1  1  1  0  1  1  1  0          1  1  1  0  1  0  0  0
        payload += [0xEE, 0xE8] # 1110

    return payload


def build_switch_msg(state, device_address=ALL_SOCKETS, house_address=None):
    """Build a message to turn a switch on or off"""
    #print("build: state:%s, device:%d, house:%s" % (str(state), device_address, str(house_address)))

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

    payload  = encode_bits((house_address & 0x0F0000) >> 16, 4)
    payload += encode_bits((house_address & 0x00FF00) >> 8,  8)
    payload += encode_bits((house_address & 0x0000FF),       8)

    #TODO: D3210 are the other way round in the message??
    #This is correct as presented by the PDF from Energenie though.
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

    payload += encode_bits(bits, 4)
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
    for i in range(number/2):
        bits = (data >> shift) & 0x03
        #print("    shift %d bits %d" % (shift, bits))
        encoded.append(ENCODER[bits])
        shift -= 2
    #print("  returns:%s" % ashex(modulated))
    return encoded


# END

