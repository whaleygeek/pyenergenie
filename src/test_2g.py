# test_2g.py  29/03/21  D.J.Whale
#
# cycle test the 2-gang light switch timing
# The purpose of this is to characterise the required burst length
# and holdoff time between messages, as the 2-gang device is a
# bit fussy with its timing.
# Note also that the type of bulb fitted in the left channel
# significantly affects the reliability of the switch.

import energenie
import time
import random
import cleanup_GPIO

# Configuration parameters for performance tuning
BURST_SIZE = 23            # (default 22)  inner times * .027s (about 27ms per burst)
BURST_COUNT = 1            # (default 2)   outer times
PRE_SILENCE = 0            # seconds between messages (now in MIHO009)
RECHARGE_SEC = 0.800       # amount of delay after transmitting, to recharge
REPEATS    = 5             # number of cycles of tx/silence
POST_SILENCE_SEC = 3.0     # silence after a complete switch cycle
RND_WINDOW_MS = 100        # 0..100ms randomised timing

# Devices under test (2 sides of the same MiHO009 2gang light switch)
LEFT = energenie.Devices.MIHO009((0x123456, 1))
LEFT.radio_config.inner_times = BURST_SIZE
LEFT.radio_config.outer_times = BURST_COUNT
LEFT.radio_config.tx_pre_silence = PRE_SILENCE

RIGHT = energenie.Devices.MIHO009((0x123456, 2))
RIGHT.radio_config.inner_times = BURST_SIZE
RIGHT.radio_config.outer_times = BURST_COUNT
RIGHT.radio_config.tx_pre_silence = PRE_SILENCE

# Another device, to test inter-device interference (intentionaly same preamble)
OOKDevice = energenie.Devices.ENER002((0x123456, 4))
FSKDevice = energenie.Devices.MIHO005(0x373)

#OTHER = energenie.Devices.MockSwitch("Mock")
OTHER = OOKDevice
#OTHER = FSKDevice

def do_switch(name, device, state):
    """Put any switch into a specific state"""
    print("%s: ->%d" % (name, state))
    st_tot = time.time()
    for i in range(REPEATS):
        print("tx burst no:%d" % (i+1))
        st = time.time()
        if state: device.turn_on()
        else:     device.turn_off()
        et = time.time()
        print("burst time:%f" % (et-st))

        print("recharge delay:%f" % RECHARGE_SEC)
        time.sleep(RECHARGE_SEC)

    print("post tx silence:%f" % POST_SILENCE_SEC)
    time.sleep(POST_SILENCE_SEC)
    et_tot = time.time()
    print("total switch time:%f" % (et_tot - st_tot))

def do_left(state):
   do_switch("LEFT", LEFT, state)

def do_right(state):
    do_switch("RIGHT", RIGHT, state)

def rnd_delay():
    """delay between 0 and N milliseconds randomly"""
    # This prevents the code syncing directly to the duty cycle of the
    # switch, and increases the chance of it missing the receive window.
    if RND_WINDOW_MS is None or RND_WINDOW_MS == 0: return
    d = random.randint(0, RND_WINDOW_MS)
    d = float(d)/1000
    print("rnd_delay:%f" % d)
    time.sleep(d)

def test_loop():
    # get the switch into a known challenging state
    print("set initial state on front panel switches")

    times = int(input("How many cycles?"))

    print("cycle testing...")
    for i in range(times):
        do_switch("left", RIGHT, False)
        rnd_delay()
        do_switch("left", RIGHT, True)
        rnd_delay()

def main():
    print("init...")
    cleanup_GPIO.cleanup()
    energenie.init()
    print("done")

    try:
        test_loop()

    finally:
        print("cleanup...")
        try:
            energenie.finished()
        finally:
            try:
                energenie.cleanup()  # forceably clean up GPIO lines
            finally:
                print("done")

if __name__ == "__main__":
    main()


