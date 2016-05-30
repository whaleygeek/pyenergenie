# control_any.py  17/03/2016  D.J.Whale
#
# Control Energenie MiHome Adaptor or AdaptorPlus sockets
# and also ENER002 legacy green button sockets.

# Shows how to use the registry to create devices.
# You should first run setup_tool.py and join some sockets

import time
import energenie

APP_DELAY = 2 # number of seconds to toggle the socket switches


#----- TEST APPLICATION -------------------------------------------------------

def socket_toggle_loop():
    """Toggle the switch on all devices in the directory"""

    global socket_state

    print("Setting socket switches to %s" % str(socket_state))

    for device in energenie.registry.devices():
        # Only try to toggle the switch for devices that actually have a switch

        if device.has_switch():
            print("  socket id %s" % device)
            device.set_switch(socket_state)

    socket_state = not socket_state
    time.sleep(APP_DELAY)


if __name__ == "__main__":
    
    print("starting socket tester (from registry)")
    energenie.init()

    socket_state = False

    try:
        while True:
            socket_toggle_loop()

    finally:
        energenie.finished()

# END
