# Registry_Test.py  21/05/2016  D.J.Whale
#
# Test harness for the Registry

#TODO: need a way to separate device creation from device restoration
#and the app needs to know what mode it is in.
#creation is probably just a test feature, as a user would either
#install the device, configure it, or learn it.


import unittest
from Registry import *
import radio
from lifecycle import *

radio.DEBUG=True

REGISTRY_KVS = "registry.kvs"

def remove_file(filename):
    import os
    try:
        os.unlink(filename)
    except OSError:
        pass # ok if it does not already exist


def show_file(filename):
    """Show the contents of a file on screen"""
    with open(filename) as f:
            for l in f.readlines():
                l = l.strip() # remove nl
                print(l)

def create_file(filename):
    with open(filename, "w"):
        pass


class TestRegistry(unittest.TestCase):

    #----- HERE -----

    @test_0
    def test_create(self):
        """Make a registry file by calling methods, and see that the file is the correct format"""
        remove_file(REGISTRY_KVS)
        create_file(REGISTRY_KVS)
        registry = DeviceRegistry(REGISTRY_KVS)

        # add some devices to the registry, it should auto update the file
        tv = Devices.MIHO005(device_id=0x68b)
        fan = Devices.ENER002(device_id=(0xC8C8C, 1))
        registry.add(tv, "tv")
        registry.add(fan, "fan")

        # see what the file looks like
        show_file(registry.DEFAULT_FILENAME)


    @test_1
    def test_load(self):
        """Load back a persisted registry and create objects from them, in the registry"""

        # create a registry file
        remove_file(REGISTRY_KVS)
        create_file(REGISTRY_KVS)
        registry = DeviceRegistry(REGISTRY_KVS)
        registry.add(Devices.MIHO005(device_id=0x68b), "tv")
        registry.add(Devices.ENER002(device_id=(0xC8C8C, 1)), "fan")
        registry.list()

        # clear the in memory registry
        registry = None

        # create and load from file
        registry = DeviceRegistry()
        registry.load_from(REGISTRY_KVS)

        # dump the registry state
        registry.list()

        #TODO loading the registry should set up receive routes also
        #perhaps we have to get the registry to do that *after* loading all objects
        #as an extra pass?
        fsk_router.list() #### FAIL no routes created by registry
        self.fail("no routes") #TODO:####


    @test_0 # DONE
    def test_load_into(self):

        # create an in memory registry
        registry = DeviceRegistry()
        registry.add(Devices.MIHO005(device_id=0x68b), "tv")
        registry.add(Devices.ENER002(device_id=(0xC8C8C, 1)), "fan")

        class MyContext():pass
        context = MyContext()

        registry.load_into(context)
        print(context.tv)
        print(context.fan)



#TODO: This is not realy a registry tester, it's a device class/router tester??
class Dis:
##class TestRegistry(unittest.TestCase):
    def setUp(self):
        # seed the registry
        registry.add(Devices.MIHO005(device_id=0x68b), "tv")
        registry.add(Devices.ENER002(device_id=(0xC8C8C, 1)), "fan")

        # test the auto create mechanism
        registry.auto_create(self)

    @test_0
    def test_capabilities(self):
        print("tv switch:%s"  % self.tv.has_switch())
        print("tv send:%s"    % self.tv.can_send())
        print("tv receive:%s" % self.tv.can_receive())

        print("fan switch:%s"  % self.fan.has_switch())
        print("fan send:%s"    % self.fan.can_send())
        print("fan receive:%s" % self.fan.can_receive())

    @test_0
    def test_ook_tx(self):
        """Test the transmit pipeline"""

        self.fan.turn_on()
        self.fan.turn_off()

    @test_0
    def test_fsk_tx(self):
        """Test the transmit pipeline for MiHome FSK devices"""

        self.tv.turn_on()
        self.tv.turn_off()

    @test_0
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



UNKNOWN_SENSOR_ID = 0x111

#TODO: Due to use of the fsk_router and registry instances,
#these tests will not run back to back yet. Have to run them one at a time.

class TestDiscovery(unittest.TestCase):
    def setUp(self):
        # build a synthetic message
        self.msg = OpenThings.Message(Devices.MIHO005_REPORT)
        self.msg[OpenThings.PARAM_VOLTAGE]["value"] = 240

    @test_0
    def test_discovery_none(self):
        discovery_none()

        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect unknown handler to fire

    @test_0
    def test_discovery_auto(self):
        discovery_auto()

        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect auto accept logic to fire
        registry.list()
        fsk_router.list()

    @test_0
    def test_discovery_ask(self):
        def yes(a,b): return True
        def no(a,b):  return False

        discovery_ask(no)

        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect a reject

        discovery_ask(yes)

        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect a accept
        registry.list()
        fsk_router.list()

    @test_0
    def test_discovery_autojoin(self):
        discovery_autojoin()

        # Poke synthetic unknown JOIN into the router and let it route to unknown handler
        msg = Devices.MIHO005.get_join_req(UNKNOWN_SENSOR_ID)

        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), msg)

        # expect auto accept and join_ack logic to fire
        registry.list()
        fsk_router.list()

    @test_0
    def test_discovery_askjoin(self):
        def no(a,b): return False
        def yes(a,b): return True

        discovery_askjoin(no)

        # Poke synthetic unknown JOIN into the router and let it route to unknown handler
        msg = Devices.MIHO005.get_join_req(UNKNOWN_SENSOR_ID)
        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), msg)

        # expect reject
        registry.list()
        fsk_router.list()

        discovery_askjoin(yes)

        fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), msg)

        # expect auto accept and join_ack logic to fire
        registry.list()
        fsk_router.list()


if __name__ == "__main__":
    import OpenThings
    OpenThings.init(Devices.CRYPT_PID)

    unittest.main()

# END