# monitor_mihome.py  27/09/2015  D.J.Whale
#
# Monitor Energine MiHome sockets

import energenie
import Logger
import time

MY_SENSOR_ID    = 0x68b # manually captured from a previous run
DUMMY_SENSOR_ID = 0x111 # for testing unknown messages


#----- TEST APPLICATION -------------------------------------------------------

if __name__ == "__main__":
    
    print("starting monitor tester")
    energenie.init()

    #TESTING
    # Manually seed the device registry and router with a known device address
    purple = energenie.Devices.MIHO005(MY_SENSOR_ID)
    energenie.registry.add(purple, "purple")
    energenie.fsk_router.add((energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), purple)

    # provide a default incoming message handler
    # This is useful for logging every message
    ##def incoming(address, message):
    ##    print("\nIncoming from %s" % str(address))
    ##    Logger.logMessage(message)
    ##energenie.fsk_router.when_incoming(incoming)

    # Provide an unknown message handler so we can show data from unregistered devices
    # This is a useful hook point for later adding device discovery
    def unknown(address, message):
        print("\nUnknown device:%s" % str(address))
        message.dump()
    energenie.fsk_router.when_unknown(unknown)

    # Register for update callbacks on a single device when a new message comes in.
    # This is a useful way to add data logging on a per-device basis
    def new_data(self, message):
        print("\nnew data for %s" % self)
        message.dump()
        Logger.logMessage(message)
    purple.when_updated(new_data)

    try:
        while True:
            #TESTING: build a synthetic message
            msg = energenie.OpenThings.Message(energenie.Devices.MIHO005_REPORT)
            msg[energenie.OpenThings.PARAM_VOLTAGE]["value"] = 240

            #TESTING: Poke synthetic unknown into the router and let it route to unknown handler
            msg.set(header_sensorid=DUMMY_SENSOR_ID)
            energenie.fsk_router.incoming_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, DUMMY_SENSOR_ID), msg)

            #TESTING: Poke synthetic known into the router and let it route to our class instance
            msg.set(header_sensorid=MY_SENSOR_ID)
            energenie.fsk_router.incoming_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), msg)

            #TODO: Knit with real radio
            # Process any received messages from the real radio
            ##energenie.loop()

            print("voltage:%s" % purple.get_voltage())
            time.sleep(1)

    finally:
        energenie.finished()

# END
