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

    def new_data(self, message):
        print("new data for %s" % self)
        message.dump()
        Logger.logMessage(message)
    purple.when_updated(new_data)

    # Override the default unknown handler, so we can show data from unregistered devices
    def unk(address, message):
        print("Unknown device:%s" % str(hex(address[2])))
        message.dump()
        #TODO: add device to registry and to fsk_router table
        #note: requires auto class create from product_id to be working first
        Logger.logMessage(message)
    energenie.fsk_router.handle_unknown = unk
    #TODO: Provide a better callback registration scheme
    ##energenie.fsk_router.when_unknown(unk)

    try:
        while True:
            #TESTING: build a synthetic message
            msg = energenie.OpenThings.Message(energenie.Devices.MIHO005_REPORT)
            msg[energenie.OpenThings.PARAM_VOLTAGE]["value"] = 240

            #TESTING: Poke synthetic unknown into the router and let it route to unknown handler
            msg.set(header_sensorid=DUMMY_SENSOR_ID)
            energenie.fsk_router.handle_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, DUMMY_SENSOR_ID), msg)

            #TESTING: Poke synthetic known into the router and let it route to our class instance
            msg.set(header_sensorid=MY_SENSOR_ID)
            energenie.fsk_router.handle_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), msg)

            #TODO: Knit with real radio
            # Process any received messages from the real radio
            ##energenie.loop()

            print("voltage:%s" % purple.get_voltage())
            time.sleep(1)

    finally:
        energenie.finished()

# END
