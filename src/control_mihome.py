# control_mihome.py  17/03/2016  D.J.Whale
#
# Control Energenie MiHome Adaptor or AdaptorPlus sockets

import energenie
from Timer import Timer

# Define this if you want to seed the registry with know device_id's for testing
# Alternatively, remove this line, and use discover_mihome.py to fill your registry
MY_SOCKET_IDS = [0x68b]

TX_RATE = 2 # number of seconds to toggle the socket switches

#----- TEST APPLICATION -------------------------------------------------------

def socket_toggle_loop():
    """Toggle the switch on all devices in the directory"""

    global socket_state

    if energenie.registry.size() > 0 and send_timer.check():
        print("Setting socket switches to %s" % str(socket_state))

        for device in energenie.registry.devices(): #TODO: Make energenie.registry iterable
            # Only try to toggle the switch for devices that actually have a switch

            if device.has_switch():
                print("  socket id %s" % device)
                device.set_switch(socket_state)

        socket_state = not socket_state


if __name__ == "__main__":
    
    print("starting socket tester")
    energenie.init()

    # Seed the registry with known devices to simplify tx-only testing
    try:
        for id in MY_SOCKET_IDS:
            socket = energenie.Devices.MIHO005(id)
            energenie.registry.add(socket, "socket_%s" % str(hex(id)))
    except:
        pass

    send_timer = Timer(TX_RATE, 1)   # every n seconds offset by initial 1
    socket_state = False

    try:
        while True:
            socket_toggle_loop()

    finally:
        energenie.finished()

# END
