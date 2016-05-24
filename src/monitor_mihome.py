# monitor_mihome.py  27/09/2015  D.J.Whale
#
# Monitor Energine MiHome sockets

import energenie
import Logger
import time

MY_SENSOR_ID = 0x68b # manually captured from a previous run
DUMMY_SENSOR_ID = 0x111 # for testing unknown messages


#----- TEST APPLICATION -------------------------------------------------------

if __name__ == "__main__":
    
    print("starting monitor tester")
    energenie.init()

    # Manually seed the device registry and router with a known device address
    purple = energenie.Devices.MIHO005(MY_SENSOR_ID)
    energenie.registry.add(purple, "purple")
    energenie.fsk_router.add((energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), purple)

    def new_data(self, message):
        print("new data for %s\n%s\n\n" % (self, message))
        Logger.logMessage(message)
    #TODO: Provide a notify callback for when our device gets new data
    ##purple.when_incoming(new_data)

    # Override the default unknown handler, so we can show data from unregistered devices
    def unk(address, message):
        print("Unknown device:%s\n%s\n\n" % (address, message))
        #TODO: add device to registry and to fsk_router table
        #note: requires auto class create from product_id to be working first
        Logger.logMessage(message)
    energenie.fsk_router.handle_unknown = unk
    #TODO: Provide a better callback registration scheme
    ##energenie.fsk_router.when_unknown(unk)

    try:
        while True:
            # Send a synthetic message to the device
            msg = energenie.OpenThings.Message(energenie.Devices.MIHO005_REPORT)
            msg[energenie.OpenThings.PARAM_VOLTAGE]["value"] = 240

            # Poke the synthetic unknown reading into the router and let it route it to the device class instance
            msg.set(header_sensorid=MY_SENSOR_ID)
            energenie.fsk_router.handle_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, DUMMY_SENSOR_ID), msg)

            # Poke the synthetic known reading into the router and let it route it to the device class instance
            msg.set(header_sensorid=DUMMY_SENSOR_ID)
            energenie.fsk_router.handle_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), msg)

            # Process any received messages from the real radio
            ##energenie.loop()

            print("purple voltage:%s" % purple.get_voltage())
            time.sleep(1)



    finally:
        energenie.finished()

# END
