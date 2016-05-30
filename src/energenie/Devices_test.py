# Devices_test.py  21/05/2016  D.J.Whale
#
# Test harness for Devices module

import unittest
from lifecycle import *

try:
    # Python 2
    import Devices
    import OpenThings
    import radio

except ImportError:
    # Python 3
    from . import Devices
    from . import OpenThings
    from . import radio

class TestDevices(unittest.TestCase):

    @test_1
    def test_without_registry(self):
        """A simple on/off test with some devices from the device factory"""
        tv   = Devices.DeviceFactory.get_device_from_name("GreenButton", device_id=(0xC8C8C, 1))
        fan  = Devices.DeviceFactory.get_device_from_name("AdaptorPlus", device_id=0x68b)
        xbox = Devices.DeviceFactory.get_device_from_id(Devices.PRODUCTID_MIHO005, device_id=10)

        print("ON")
        tv.turn_on()
        fan.turn_off()
        xbox.turn_off()

        print("OFF")
        tv.turn_off()
        fan.turn_on()
        xbox.turn_on()

    @test_1
    def test_rx_seq(self):
        """Test that the rx sequence increments on each received message"""
        fan  = Devices.DeviceFactory.get_device_from_name("AdaptorPlus", device_id=0x68b)

        msg = OpenThings.Message(Devices.MIHO005_REPORT)
        print(fan.get_receive_count())

        fan.incoming_message(msg)
        print(fan.get_receive_count())


def init():
    """Start the Energenie system running"""
    radio.DEBUG = True
    radio.init()
    OpenThings.init(Devices.CRYPT_PID)


if __name__ == "__main__":
    init()
    unittest.main()

# END

