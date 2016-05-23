# Registry_Test.py  21/05/2016  D.J.Whale
#
# Test harness for the Registry

#TODO: need a way to separate device creation from device restoration
#and the app needs to know what mode it is in.
#creation is probably just a test feature, as a user would either
#install the device, configure it, or learn it.


import unittest
from Registry import *

class TestRegistry(unittest.TestCase):
    def setUp(self):
        # seed the registry
        registry.add(Devices.MIHO005(device_id=0x68b), "tv")
        registry.add(Devices.ENER002(device_id=(0xC8C8C, 1)), "fan")

        # test the auto create mechanism
        #import sys
        #registry.auto_create(sys.modules[__name__])
        registry.auto_create(self)

    def test_capabilities(self):
        print("tv switch:%s"  % self.tv.has_switch())
        print("tv send:%s"    % self.tv.can_send())
        print("tv receive:%s" % self.tv.can_receive())

        print("fan switch:%s"  % self.fan.has_switch())
        print("fan send:%s"    % self.fan.can_send())
        print("fan receive:%s" % self.fan.can_receive())

    def test_ook_tx(self):
        """Test the transmit pipeline"""

        self.fan.turn_on()
        self.fan.turn_off()

    def test_fsk_tx(self):
        """Test the transmit pipeline for MiHome FSK devices"""

        self.tv.turn_on()
        self.tv.turn_off()

    def test_fsk_rx(self):
        """Test the receive pipeline for FSK MiHome adaptor"""

        #synthesise receiving a report message
        #push it down the receive pipeline
        #radio.receive()
        # ->OpenThingsAirInterface.incoming
        # ->OpenThings.decrypt
        # ->OpenThings.decode
        # ->OpenThingsAirInterface->route
        # ->MIHO005.incoming_message()
        #
        #it should update voltage, power etc
        ## poor mans incoming synthetic message


        report = OpenThings.Message(Devices.MIHO005_REPORT)
        report.set(recs_VOLTAGE_value=240,
                   recs_CURRENT_value=2,
                   recs_FREQUENCY_value=50,
                   recs_REAL_POWER_value=100,
                   recs_REACTIVE_POWER_value=0,
                   recs_APPARENT_POWER_value=100)
        self.tv.incoming_message(report)

        # get readings from device
        voltage   = self.tv.get_voltage()
        frequency = self.tv.get_frequency()
        power     = self.tv.get_real_power()
        switch    = self.tv.is_on()

        print("voltage %f"    % voltage)
        print("frequency %f"  % frequency)
        print("real power %f" % power)
        print("switch %s"     % switch)


if __name__ == "__main__":
    import OpenThings
    OpenThings.init(Devices.CRYPT_PID)

    unittest.main()

# END