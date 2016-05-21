# Devices_test.py  21/05/2016  D.J.Whale
#
# Test harness for Devices module

#TODO: Turn into unittest.TestCase


import time
from Devices import *

#hmm: need two addresses for legacy - use a tuple (house_address, index)

#unless we have an adaptor class for air_interface which represents the
#collective house address for a house code. So if you use more than one
#house address, you create multiple air interface adaptors with different
#house codes, that just delegate to the same actual radio air interface?
#bit like a little local router?

#legacy1 = AirInterface.create("OOK", address=0xC8C8C, energenie_radio)

# Could also consider this a local network, with common parameters shared
# by all devices that use it.
#air2    = AirInterface.create("FSK", energenie_radio)

# scheduling would then become
# scheduler = Scheduler(energenie_radio)
# legacy1 = AirInterface.create("OOK", address=0xC8C8C, scheduler)
# air2    = AirInterface.create("FSK", scheduler
# so that when a device tries to transmit, it gets air interface specific
# settings added to it as appropriate, then the scheduler decides when
# to send and receive

# Somehow we need to associate devices with an air interface
# This might allow us to support multiple radios in the future too?
#legacy1.add(tv)

# cooperative loop could be energenie_radio.loop()
# or wrap a thread around it with start() but beware of thread context
# and thread safety.


def test_without_registry():

    ##TODO: Problem, some devices have air_interface, some have adaptor, some have nothing,
    #so the DeviceFactory constructor (c) doesn't work correctly with all devices
    tv  = DeviceFactory.get_device("GreenButton", device_id=(0xC8C8C, 1))
    fan = DeviceFactory.get_device("AdaptorPlus", device_id=0x68b)

    while True:
        print("ON")
        tv.turn_on()
        fan.turn_off()
        time.sleep(2)

        print("OFF")
        tv.turn_off()
        fan.turn_on()
        time.sleep(1)


if __name__ == "__main__":
    test_without_registry()

# END

