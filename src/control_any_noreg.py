# control_any_noreg.py  17/03/2016  D.J.Whale
#
# Control up to 4 legacy green-button sockets (or MiHome control-only sockets)
# Shows how to address sockets directly without using the registry.

import time
import energenie

APP_DELAY = 1

# Devices that use the standard Energenie house code
all_sockets = energenie.Devices.ENER002(0)
socket1     = energenie.Devices.ENER002(1)
socket2     = energenie.Devices.ENER002(2)
socket3     = energenie.Devices.ENER002(3)
socket4     = energenie.Devices.ENER002(4)

# A device that uses a custom house code (e.g. learnt from a hand controller)
socket5     = energenie.Devices.ENER002((0x1234, 1))

# A MiHome device that we know the address of from a previous capture
socket6     = energenie.Devices.MIHO005(0x68b)

sockets     = [all_sockets, socket1, socket2, socket3, socket4, socket5, socket6]


def legacy_socket_loop():
    """Turn all sockets on or off every few seconds"""

    while True:
        for socket_no in range(len(sockets)):
            # socket_no 0 is ALL, then 1=1, 2=2, 3=3, 4=4
            # ON
            print("socket %d ON" % socket_no)
            sockets[socket_no].turn_on()
            time.sleep(APP_DELAY)

            # OFF
            print("socket %d OFF" % socket_no)
            sockets[socket_no].turn_off()
            time.sleep(APP_DELAY)


if __name__ == "__main__":
    print("starting socket tester (no registry)")

    energenie.init()

    try:
        legacy_socket_loop()
    finally:
        energenie.finished()

# END

