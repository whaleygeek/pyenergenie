# monitor_mihome.py  27/09/2015  D.J.Whale
#
# Monitor Energine MiHome sockets

import energenie
import Logger
import time


#----- TEST APPLICATION -------------------------------------------------------

if __name__ == "__main__":
    
    print("starting monitor tester")
    energenie.init()

    # Manually seed the device registry and router with a known device address
    purple = energenie.Devices.MIHO005(0x68b)
    energenie.registry.add(purple, "purple")
    energenie.fsk_router.add((energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005,0x68b), purple)

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
            energenie.fsk_router.handle_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, 0x111), msg)

            # Poke the synthetic known reading into the router and let it route it to the device class instance
            energenie.fsk_router.handle_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, 0x68b), msg)

            # Process any received messages from the real radio
            ##energenie.loop()

            print("purple voltage:%s" % purple.get_voltage())
            time.sleep(1)



    finally:
        energenie.finished()

# END
