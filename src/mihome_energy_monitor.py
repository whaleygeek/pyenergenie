# mihome_energy_monitor.py  28/05/2016  D.J.Whale
#
# A simple demo of monitoring and logging energy usage of mihome devices

# NOTE: This will eventually replace monitor_mihome.py

# REQUIREMENTS:
#   receive updates from any registered device in the registry
#   show friendly data update messages on the screen
#   store data updates to the log file



# monitor_mihome.py  27/09/2015  D.J.Whale
#
# Monitor Energine MiHome sockets

#NOTE: This file will soon be deprecated, and replaced with mihome_energy_monitor.py




import energenie
##import Logger
import time

APP_DELAY         = 5
MY_SENSOR_ID      = 0x68b #TESTING
UNKNOWN_SENSOR_ID = 0x111 #TESTING

energenie.radio.DEBUG = True

#----- TEST APPLICATION -------------------------------------------------------

if __name__ == "__main__":

    print("starting monitor tester")
    energenie.init()

    #TESTING
    # Manually seed the device registry and router with a known device address
    ##purple = energenie.Devices.MIHO005(MY_SENSOR_ID)
    ##energenie.registry.add(purple, "purple")
    ##energenie.fsk_router.add((energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), purple)

    # provide a default incoming message handler
    # This is useful for logging every message
    ##def incoming(address, message):
    ##    print("\nIncoming from %s" % str(address))
    ##    Logger.logMessage(message)
    ##energenie.fsk_router.when_incoming(incoming)

    # Register for update callbacks on a single device when a new message comes in.
    # This is a useful way to add data logging on a per-device basis
    ##def new_data(self, message):
    ##    print("\nnew data for %s" % self)
    ##    message.dump()
    ##    Logger.logMessage(message)
    ##purple.when_updated(new_data)

    #TESTING: build a synthetic message
    report_msg = energenie.OpenThings.Message(energenie.Devices.MIHO005_REPORT)
    report_msg[energenie.OpenThings.PARAM_VOLTAGE]["value"] = 240

    #TESTING: Poke a synthetic join request coming from a device id
    # With the default discovery_autojoin this should enter it into the registry
    join_msg = energenie.Devices.MIHO005.get_join_req(MY_SENSOR_ID)
    energenie.fsk_router.incoming_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), join_msg
    )

    energenie.registry.list()
    energenie.fsk_router.list()

    switch_state = True

    try:
        while True:

            #TESTING: Poke synthetic unknown into the router and let it route to unknown handler
            ##print("synthetic unknown device")
            ##report_msg.set(header_sensorid=UNKNOWN_SENSOR_ID)
            ##energenie.fsk_router.incoming_message(
            ##    (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, UNKNOWN_SENSOR_ID), report_msg)

            #TESTING: Poke synthetic known into the router and let it route to our class instance
            print("synthetic known device")
            report_msg.set(header_sensorid=MY_SENSOR_ID)
            energenie.fsk_router.incoming_message(
                (energenie.Devices.MFRID_ENERGENIE, energenie.Devices.PRODUCTID_MIHO005, MY_SENSOR_ID), report_msg)

            #TODO: Knit with real radio
            # Process any received messages from the real radio
            ##energenie.loop()

            # For all devices in the registry, if they offer a power reading, display it
            #TODO

            # For all devices in the registry, if they have a switch, toggle it
            for d in energenie.registry.devices():
                if d.has_switch():
                    d.set_switch(switch_state)
            switch_state = not switch_state

            ##print("voltage:%s" % purple.get_voltage())
            time.sleep(APP_DELAY)

    finally:
        energenie.finished()

# END

