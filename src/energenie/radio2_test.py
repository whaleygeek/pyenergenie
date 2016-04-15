# radio2_test.py  15/04/2016  D.J.Whale
#
# A simple Energenie radio exerciser
#
# Repeatedly transmits OOK packets to turn switch 1 on and off.
#

import radio2 as radio
import time

# How many times to repeat the OOK payload.
# NOTE: At the moment this is limited to 16*8<256 in the HRF module
# but that restriction will soon be removed.


REPEATS = 8


# The 'radio' module knows nothing about the Energenie (HS1527) bit encoding,
# so this test code manually encodes the bits.
# For the full Python stack, there is an encoder module that can generate
# specific payloads. Repeats are done in radio_transmitter.
# The HRF preamble feature is no longer used, it's more predictable to
# put the preamble in the payload.


# preamble pulse with timing violation gap
PREAMBLE = [0x80, 0x00, 0x00, 0x00]

# Energenie 'random' 20 bit address is 0x6C6C6
# 0110 1100 0110 1100 0110
# 0 encoded as 8 (1000)
# 1 encoded as E (1110)
ADDR     = [0x8E, 0xE8, 0xEE, 0x88, 0x8E, 0xE8, 0xEE, 0x88, 0x8E, 0xE8]

# Energenie 'switch 1 ON' command  F 1111  (0xEE, 0xEE)
SW1_ON  = [0xEE, 0xEE]

# Energenie 'switch 1 OFF' command E 1110  (0xEE, 0xE8)
SW1_OFF = [0xEE, 0xE8]

# manual preamble, 20 bit encoded address, 4 encoded data bits
enc_1on  = PREAMBLE + ADDR + SW1_ON
enc_1off = PREAMBLE + ADDR + SW1_OFF


def radio_test_ook():
    """Repeatedly test switch 1 ON then OFF"""

    radio.init()

    try:
        radio.modulation(ook=True)
        while True:
            print("Switch 1 ON")
            radio.send_payload(enc_1on, REPEATS)
            radio.standby()
            time.sleep(1)

            print("Switch 1 OFF")
            radio.send_payload(enc_1off, REPEATS)
            radio.standby()
            time.sleep(1)
    finally:
        radio.finished()


if __name__ == "__main__":
    radio_test_ook()

# END