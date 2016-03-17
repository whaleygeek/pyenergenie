# legacy.py  17/03/2016  D.J.Whale
#
# Placeholder for a legacy plug (OOK) test harness
#
# This is a temporary piece of code, that will be thrown away once the device object interface
# is written.
#
# Please don't use this as the basis for an application, it is only designed to be used
# to test the lower level code.

# switch.py  17/03/2016  D.J.Whale
#
# Control Energenie switches.
# Note, at the moment, this only works with MiHome Adaptor Plus devices
# because the 'sensorid' is discovered via the monitor message.
# You could probably fake it by preloading the directory with your sensorid
# if you know what it is.

# Note, this is *only* a test program, to exercise the lower level code.
# Don't expect this to be a good starting point for an application.
# Consider waiting for me to finish developing the device object interface first.

import time

from energenie import  Devices, radio
from energenie import radio
from Timer import Timer

TX_RATE = 10 # seconds between each switch change cycle

def warning(msg):
    print("warning:%s" % str(msg))

def trace(msg):
    print("monitor:%s" % str(msg))


#----- TEST APPLICATION -------------------------------------------------------

def legacy_switch_loop():
    """Listen to sensor messages, and turn switches on and off every few seconds"""

    radio.transmitter(ook=True)

    # Transmit a code multiple times and program it into the switch
    print("Press the LEARN button on the switch for 5 secs until LED flashes")
    raw_input("press ENTER when LED is flashing")

    ON = radio.build_OOK_relay_msg(True)
    OFF = radio.build_OOK_relay_msg(False)

    while True:
        print("sending ON")
        radio.send_payload_repeat(ON, 8)
        print("waiting")
        time.sleep(2)

        print("sending OFF")
        radio.send_payload_repeat(OFF, 8)
        print("waiting")
        time.sleep(2)


if __name__ == "__main__":

    trace("starting legacy switch tester")
    radio.init()

    try:
        legacy_switch_loop()

    finally:
        radio.finished()

# END


# END

