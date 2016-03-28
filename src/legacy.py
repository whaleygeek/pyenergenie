# legacy.py  17/03/2016  D.J.Whale
#
# Simple legacy plug test harness.
# Legacy plugs have a big green button on the front,
# and usually come in kits with a handheld remote control.
#
# Note: This is a temporary piece of code, that will be thrown away
# once the device object interface is written.
#
# Please don't use this as the basis for an application,
# it is only designed to be used to test the lower level code.

import time

from energenie import encoder
from energenie import radio


#----- TEST APPLICATION -------------------------------------------------------

# Prebuild all possible message up front, to make switching code faster

HOUSE_ADDRESS = None # default

ALL_ON     = encoder.build_switch_msg(True,                    house_address=HOUSE_ADDRESS)
ONE_ON     = encoder.build_switch_msg(True,  device_address=1, house_address=HOUSE_ADDRESS)
TWO_ON     = encoder.build_switch_msg(True,  device_address=2, house_address=HOUSE_ADDRESS)
THREE_ON   = encoder.build_switch_msg(True,  device_address=3, house_address=HOUSE_ADDRESS)
FOUR_ON    = encoder.build_switch_msg(True,  device_address=4, house_address=HOUSE_ADDRESS)
ON_MSGS    = [ALL_ON, ONE_ON, TWO_ON, THREE_ON, FOUR_ON]

ALL_OFF    = encoder.build_switch_msg(False,                   house_address=HOUSE_ADDRESS)
ONE_OFF    = encoder.build_switch_msg(False, device_address=1, house_address=HOUSE_ADDRESS)
TWO_OFF    = encoder.build_switch_msg(False, device_address=2, house_address=HOUSE_ADDRESS)
THREE_OFF  = encoder.build_switch_msg(False, device_address=3, house_address=HOUSE_ADDRESS)
FOUR_OFF   = encoder.build_switch_msg(False, device_address=4, house_address=HOUSE_ADDRESS)
OFF_MSGS   = [ALL_OFF, ONE_OFF, TWO_OFF, THREE_OFF, FOUR_OFF]


def get_yes_no():
    """Get a simple yes or no answer"""
    answer = raw_input() # python2
    if answer.upper() in ['Y', 'YES']:
        return True
    return False


def legacy_learn_mode():
    """Give the user a chance to learn any switches"""
    print("Do you want to program any switches?")
    y = get_yes_no()
    if not y:
        return

    for switch_no in range(1,5):
        print("Learn switch %d?" % switch_no)
        y = get_yes_no()
        if y:
            print("Press the LEARN button on any switch %d for 5 secs until LED flashes" % switch_no)
            raw_input("press ENTER when LED is flashing")

            for i in range(8):
                print("ON")
                radio.transmit(ON_MSGS[switch_no])
                time.sleep(1)

            print("Device should now be programmed")
            
            print("Testing....")
            for i in range(4):
                time.sleep(1)
                print("OFF")
                radio.transmit(OFF_MSGS[switch_no])
                time.sleep(1)
                print("ON")
                radio.transmit(ON_MSGS[switch_no])
            print("Test completed")


def legacy_switch_loop():
    """Turn all switches on or off every few seconds"""

    while True:
        print("sending ALL ON")
        radio.transmit(ALL_ON)
        print("waiting")
        time.sleep(2)

        print("sending ALL OFF")
        radio.transmit(ALL_OFF)
        print("waiting")
        time.sleep(2)


def legacy_test():
    #TODO: This testing shows that the C code and the specs are out of step
    #ONE_ON = encoder.build_relay_msg(True)
    #ONE_OFF = encoder.build_relay_msg(False)
    ONE_ON  = encoder.build_switch_msg(True, device_address=1)
    ONE_OFF = encoder.build_switch_msg(False, device_address=1)

    while True:
        print("ON")
        radio.transmit(ONE_ON)
        time.sleep(1)
    
        print("OFF")
        radio.transmit(ONE_OFF)
        time.sleep(1)


if __name__ == "__main__":

    print("starting legacy switch tester")
    radio.init()
    radio.transmitter(ook=True)

    try:
        #legacy_learn_mode()
        #legacy_switch_loop()
        legacy_test()

    finally:
        radio.finished()


# END

