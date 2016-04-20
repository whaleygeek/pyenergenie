# legacy.py  17/03/2016  D.J.Whale
#
# Note: This is a test harness only, to prove that the underlying OOK
# radio support for legacy plugs is working.
# Please don't use this as a basis for building your applications from.
# Another higher level device API will be designed once this has been
# completely verified.

import time

from energenie import encoder
# moving over to the new, faster, C radio driver
from energenie import radio2 as radio

# How many times to send messages in the driver fast loop
# Present version of driver limits to 15
# but this restriction will be lifted soon
# 4800bps, burst transmit time at 15 repeats is 400mS
# 1 payload takes 26ms
# 75 payloads takes 2s
INNER_TIMES = 8

# how many times to send messages in the API slow loop
# this is slower than using the driver, and will introduce
# inter-burst delays
OUTER_TIMES = 1

# delay in seconds between each application switch message
APP_DELAY = 1

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

            print("ON")
            radio.transmit(ON_MSGS[switch_no], OUTER_TIMES, INNER_TIMES)
            time.sleep(APP_DELAY)

            print("Device should now be programmed")
            
            print("Testing....")
            for i in range(4):
                time.sleep(APP_DELAY)
                print("OFF")
                radio.transmit(OFF_MSGS[switch_no], OUTER_TIMES, INNER_TIMES)
                time.sleep(APP_DELAY)
                print("ON")
                radio.transmit(ON_MSGS[switch_no], OUTER_TIMES, INNER_TIMES)
            print("Test completed")


def legacy_switch_loop():
    """Turn all switches on or off every few seconds"""

    while True:
        for switch_no in range(5):
            # switch_no 0 is ALL, then 1=1, 2=2, 3=3, 4=4
            # ON
            print("switch %d ON" % switch_no)
            radio.transmit(ON_MSGS[switch_no], OUTER_TIMES, INNER_TIMES)
            time.sleep(APP_DELAY)

            # OFF
            print("switch %d OFF" % switch_no)
            radio.transmit(OFF_MSGS[switch_no], OUTER_TIMES, INNER_TIMES)
            time.sleep(APP_DELAY)
        
def switch1_loop():
    """Repeatedly turn switch 1 ON then OFF"""
    while True:
        print("Switch all ON")
        radio.transmit(ON_MSGS[0], OUTER_TIMES, INNER_TIMES)
        time.sleep(APP_DELAY)

        print("Switch all OFF")
	radio.transmit(OFF_MSGS[0], OUTER_TIMES, INNER_TIMES)
        time.sleep(APP_DELAY)


def pattern_test():
    """Test all patterns"""
    while True:
        p = raw_input("number 0..F")
        p = int(p, 16)
        msg = encoder.build_test_message(p)
        print("pattern %s payload %s" % (str(hex(p)), encoder.ashex(msg)))
        radio.send_payload(msg, OUTER_TIMES, INNER_TIMES)
            

if __name__ == "__main__":

    print("starting legacy switch tester")
    print("radio init")
    radio.init()
    print("radio as OOK")
    radio.modulation(ook=True)

    try:
        #pattern_test()
        #legacy_learn_mode()
        #legacy_switch_loop()
        switch1_loop()
    finally:
        radio.finished()


# END

