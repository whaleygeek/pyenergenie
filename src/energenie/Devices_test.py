# Devices_test.py  21/05/2016  D.J.Whale
#
# Test harness for Devices module

#TODO: Turn into unittest.TestCase


import time
from Devices import *

# cooperative loop could be energenie_radio.loop()
# or wrap a thread around it with start() but beware of thread context
# and thread safety.

import radio
radio.DEBUG = True

def test_without_registry():

    tv   = DeviceFactory.get_device_from_name("GreenButton", device_id=(0xC8C8C, 1))
    fan  = DeviceFactory.get_device_from_name("AdaptorPlus", device_id=0x68b)
    xbox = DeviceFactory.get_device_from_id(PRODUCTID_MIHO005, device_id=10)

    while True:
        print("ON")
        tv.turn_on()
        fan.turn_off()
        xbox.turn_off()
        time.sleep(2)

        print("OFF")
        tv.turn_off()
        fan.turn_on()
        xbox.turn_on()
        time.sleep(1)


if __name__ == "__main__":
    import OpenThings, Devices
    OpenThings.init(Devices.CRYPT_PID)
    test_without_registry()

# END

