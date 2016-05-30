# mihome_energy_monitor.py  28/05/2016  D.J.Whale
#
# A simple demo of monitoring and logging energy usage of mihome devices
#
# Logs all messages to screen and to a file energenie.csv
# Any device that has a switch, it toggles it every 2 seconds.
# Any device that offers a power reading, it displays it.

import energenie
import Logger
import time

APP_DELAY    = 2
switch_state = False

def energy_monitor_loop():
    global switch_state

    # Process any received messages from the real radio
    energenie.loop()

    # For all devices in the registry, if they have a switch, toggle it
    for d in energenie.registry.devices():
        if d.has_switch():
            d.set_switch(switch_state)
    switch_state = not switch_state

    # For all devices in the registry, if they have a get_power(), call it
    print("Checking device status")
    for d in energenie.registry.devices():
        print(d)
        try:
            p = d.get_power()
            print("Power: %s" % str(p))
        except:
            pass # Ignore it if can't provide a power

    time.sleep(APP_DELAY)


if __name__ == "__main__":

    print("Starting energy monitor example")

    energenie.init()

    # provide a default incoming message handler, useful for logging every message
    def incoming(address, message):
        print("\nIncoming from %s" % str(address))
        Logger.logMessage(message)
    energenie.fsk_router.when_incoming(incoming)
    print("Logging to file:%s" % Logger.LOG_FILENAME)

    try:
        while True:
            energy_monitor_loop()
    finally:
        energenie.finished()

# END

