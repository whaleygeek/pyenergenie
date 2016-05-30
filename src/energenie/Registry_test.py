# Registry_Test.py  21/05/2016  D.J.Whale
#
# Test harness for the Registry
# includes: DeviceRegistry, Router, Discovery

import unittest
from Registry import *
import radio
from lifecycle import *

radio.DEBUG=True

REGISTRY_KVS = "registry.kvs"


#----- FILE HELPERS -----------------------------------------------------------
#
#TODO: This is repeated in KVS_test.py

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


#----- TEST REGISTRY ----------------------------------------------------------

class TestRegistry(unittest.TestCase):

    @test_1
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
        fsk_router = Router("fsk")
        registry.set_fsk_router(fsk_router)
        registry.load_from(REGISTRY_KVS)

        # dump the registry state
        registry.list()

        # get device intances, this will cause receive routes to be knitted up
        tv = registry.get("tv")
        fan = registry.get("fan")
        registry.fsk_router.list()


    @test_1
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


#----- TEST ROUTER ------------------------------------------------------------

class TestRouter(unittest.TestCase):
    def setUp(self):
        # seed the registry
        registry = DeviceRegistry()
        registry.add(Devices.MIHO005(device_id=0x68b), "tv")
        registry.add(Devices.ENER002(device_id=(0xC8C8C, 1)), "fan")

        # test the auto create mechanism
        registry.load_into(self)

    @test_1
    def test_capabilities(self):
        print("tv switch:%s"  % self.tv.has_switch())
        print("tv send:%s"    % self.tv.can_send())
        print("tv receive:%s" % self.tv.can_receive())

        print("fan switch:%s"  % self.fan.has_switch())
        print("fan send:%s"    % self.fan.can_send())
        print("fan receive:%s" % self.fan.can_receive())

    @test_1
    def test_ook_tx(self):
        """Test the transmit pipeline"""

        self.fan.turn_on()
        self.fan.turn_off()

    @test_1
    def test_fsk_tx(self):
        """Test the transmit pipeline for MiHome FSK devices"""

        self.tv.turn_on()
        self.tv.turn_off()

    @test_1
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
        # poor mans incoming synthetic message


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


#----- TEST DISCOVERY ---------------------------------------------------------

UNKNOWN_SENSOR_ID = 0x111

class TestDiscovery(unittest.TestCase):
    def setUp(self):
        # build a synthetic message
        self.msg = OpenThings.Message(Devices.MIHO005_REPORT)
        self.msg[OpenThings.PARAM_VOLTAGE]["value"] = 240

        self.fsk_router = Router("fsk")

        #OOK receive not yet written
        #It will be used to be able to learn codes from Energenie legacy hand remotes
        ##ook_router = Registry.Router("ook")

        self.registry = DeviceRegistry()
        self.registry.set_fsk_router(self.fsk_router)

    @test_1
    def test_discovery_none(self):
        self.fsk_router.when_unknown(None) # Discovery NONE


        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect unknown handler to fire

    @test_1
    def test_discovery_auto(self):
        d = AutoDiscovery(self.registry, self.fsk_router) # Discovery AUTO

        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect auto accept logic to fire
        self.registry.list()
        self.fsk_router.list()

    @test_1
    def test_discovery_ask(self):
        def yes(a,b): return True
        def no(a,b):  return False

        d = ConfirmedDiscovery(self.registry, self.fsk_router, no) # Discovery ASK(NO)


        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect a reject

        d = ConfirmedDiscovery(self.registry, self.fsk_router, yes) # Discovery ASK(YES)

        # Poke synthetic unknown into the router and let it route to unknown handler
        self.msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), self.msg)

        # expect a accept
        self.registry.list()
        self.fsk_router.list()

    @test_1
    def test_discovery_autojoin(self):
        d = JoinAutoDiscovery(self.registry, self.fsk_router) # Discovery AUTO JOIN

        # Poke synthetic unknown JOIN into the router and let it route to unknown handler
        msg = Devices.MIHO005.get_join_req(UNKNOWN_SENSOR_ID)

        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), msg)

        # expect auto accept and join_ack logic to fire
        self.registry.list()
        self.fsk_router.list()

    @test_1
    def test_discovery_askjoin(self):
        def no(a,b): return False
        def yes(a,b): return True

        d = JoinConfirmedDiscovery(self.registry, self.fsk_router, no) # Discovery ASK JOIN(NO)

        # Poke synthetic unknown JOIN into the router and let it route to unknown handler
        msg = Devices.MIHO005.get_join_req(UNKNOWN_SENSOR_ID)
        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), msg)

        # expect reject
        self.registry.list()
        self.fsk_router.list()

        d = JoinConfirmedDiscovery(self.registry, self.fsk_router, yes) # Discovery ASK JOIN(YES)

        self.fsk_router.incoming_message(
            (Devices.MFRID_ENERGENIE, Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), msg)

        # expect auto accept and join_ack logic to fire
        self.registry.list()
        self.fsk_router.list()


if __name__ == "__main__":
    import OpenThings
    OpenThings.init(Devices.CRYPT_PID)

    unittest.main()

# END