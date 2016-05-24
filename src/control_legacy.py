# legacy.py  17/03/2016  D.J.Whale
#
# Control up to 4 legacy green-button sockets (or MiHome control-only sockets)

import time
import energenie

APP_DELAY = 1
##energenie.radio.DEBUG = True

all_sockets = energenie.Devices.ENER002(0)
socket1     = energenie.Devices.ENER002(1)
socket2     = energenie.Devices.ENER002(2)
socket3     = energenie.Devices.ENER002(3)
socket4     = energenie.Devices.ENER002(4)
sockets     = [all_sockets, socket1, socket2, socket3, socket4]


try:
    readin = raw_input # Python 2
except NameError:
    readin = input # Python 3


def get_yes_no():
    """Get a simple yes or no answer"""
    answer = readin()
    if answer.upper() in ['Y', 'YES']:
        return True
    return False


def legacy_learn_mode():
    """Give the user a chance to learn any sockets"""
    print("Do you want to program any sockets?")
    y = get_yes_no()
    if not y:
        return

    for socket_no in range(1,5):
        print("Learn socket %d?" % socket_no)
        y = get_yes_no()
        if y:
            print("Press the LEARN button on any socket %d for 5 secs until LED flashes" % socket_no)
            readin("press ENTER when LED is flashing")

            print("ON")
            sockets[1].turn_on()
            time.sleep(APP_DELAY)

            print("Device should now be programmed")
            
            print("Testing....")
            for i in range(4):
                time.sleep(APP_DELAY)
                print("OFF")
                sockets[socket_no].turn_off()

                time.sleep(APP_DELAY)
                print("ON")
                sockets[socket_no].turn_on()

            print("Test completed")


def legacy_socket_loop():
    """Turn all sockets on or off every few seconds"""

    while True:
        for socket_no in range(5):
            # socket_no 0 is ALL, then 1=1, 2=2, 3=3, 4=4
            # ON
            print("socket %d ON" % socket_no)
            sockets[socket_no].turn_on()
            time.sleep(APP_DELAY)

            # OFF
            print("socket %d OFF" % socket_no)
            sockets[socket_no].turn_off()
            time.sleep(APP_DELAY)


def socket1_loop():
    """Repeatedly turn socket 1 ON then OFF"""
    while True:
        print("Plug 1 ON")
        sockets[1].turn_on()
        time.sleep(APP_DELAY)

        print("Plug 1 OFF")
        sockets[1].turn_off()
        time.sleep(APP_DELAY)

if __name__ == "__main__":
    print("starting legacy socket tester")
    energenie.init()

    try:
        legacy_learn_mode()
        legacy_socket_loop()
        ##socket1_loop()
    finally:
        energenie.finished()

# END

