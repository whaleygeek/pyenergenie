# combined.py  15/05/2016  D.J.Whale
#
# A simple demo of combining both FSK (MiHome) and OOK (green button legacy)
#
# NOTE: This is only a test harness.
# If you really want a nice way to control these devices, wait for the 'device classes'
# issues to be implemented and tested on top of the raw radio interface, as these
# will be much nicer to use.

import time
from energenie import Messages, OpenThings, radio, encoder, Devices

# build FSK messages for MiHome purple

OpenThings.init(Devices.CRYPT_PID)

PURPLE_ID = 0x68B # captured from a real device using Monitor.py
m = OpenThings.alterMessage(
    Messages.SWITCH,
    header_sensorid=PURPLE_ID,
    recs_0_value=1)
purple_on = OpenThings.encode(m)

m = OpenThings.alterMessage(
    Messages.SWITCH,
    header_sensorid=PURPLE_ID,
    recs_0_value=0)
purple_off = OpenThings.encode(m)

# build OOK messages for legacy green button

GREEN_ON  = encoder.build_switch_msg(True, device_address=1)
GREEN_OFF = encoder.build_switch_msg(False, device_address=1)


def switch_loop():
    print("Turning green ON")
    radio.modulation(ook=True)
    radio.transmit(GREEN_ON)
    time.sleep(0.5)

    print("Turning purple ON")
    radio.modulation(fsk=True)
    radio.transmit(purple_on, inner_times=2)
    time.sleep(2)

    print("Turning green OFF")
    radio.modulation(ook=True)
    radio.transmit(GREEN_OFF)
    time.sleep(0.5)

    print("Turning purple OFF")
    radio.modulation(fsk=True)
    radio.transmit(purple_off, inner_times=2)
    time.sleep(2)


if __name__ == "__main__":

    print("starting combined switch tester")
    print("radio init")
    radio.init()

    try:
        while True:
            switch_loop()

    finally:
        radio.finished()

# END
