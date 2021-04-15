# test_2g.py  29/03/21  D.J.Whale
#
# cycle test the 2-gang light switch timing
# The purpose of this is to characterise the required burst length
# and holdoff time between messages, as the 2-gang device is a
# bit fussy with its timing.

import energenie
import time
import random

# Configuration parameters for performance tuning
BURST_SIZE = 22     # (default 22)  inner times * .027s (about 27ms per burst)
BURST_COUNT = 2     # (default 2)   outer times
HOLDOFF = 3         # 3 seconds between messages
RND_WINDOW_MS = 100 # 0..100ms randomised timing

# Devices under test (2 sides of the same MiHO009 2gang light switch)
LEFT = energenie.Devices.MIHO009((0x123456, 1))
LEFT.radio_config.inner_times = BURST_SIZE
LEFT.radio_config.outer_times = BURST_COUNT

RIGHT = energenie.Devices.MIHO009((0x123456, 2))
RIGHT.radio_config.inner_times = BURST_SIZE
RIGHT.radio_config.outer_times = BURST_COUNT

# Another device, to test inter-device interference (intentionaly same preamble)
OOKDevice = energenie.Devices.ENER002((0x123456, 4))
FSKDevice = energenie.Devices.MIHO005(0x373)

OTHER = energenie.Devices.MockSwitch("Mock")
#OTHER = OOKDevice
#OTHER = FSKDevice

def do_switch(name, device, state):
    """Put any switch into a specific state"""
    print("%s:%d" % (name, state))
    st = time.time()
    if state:
        while device.turn_on():
            pass
    else:
        while device.turn_off():
            pass
    et = time.time()
    print("burst time:%f" % (et-st))

def do_left(state):
    do_switch("LEFT", LEFT, state)

def do_right(state):
    do_switch("RIGHT", RIGHT, state)

def rnd_delay():
    """delay between 0 and N milliseconds randomly"""
    # This prevents the code syncing directly to the duty cycle of the
    # switch, and increases the chance of it missing the receive window.
    d = random.randint(0, RND_WINDOW_MS)
    d = float(d)/1000
    print("rnd_delay:%f" % d)
    time.sleep(d)

def interfere(state, delay):
    """Send interference messages on another device, for a time"""
    do_until = time.time() + delay
    time.sleep(0.5)  # gap to allow OTHER to work
    while time.time() < do_until:
        if state:
            print("OTHER on")
            OTHER.turn_on()
        else:
            print("OTHER off")
            OTHER.turn_off()

def cycle(delay):
    """Do one cycle test of on/off of both switch sides"""
    do_left(True)
    interfere(True, delay)
    rnd_delay()
    do_right(True)
    interfere(False, delay)
    rnd_delay()

    do_left(False)
    interfere(True, delay)
    rnd_delay()
    do_right(False)
    interfere(False, delay)
    rnd_delay()

def test_loop():
    while True:
        cycle(HOLDOFF)

def main():
    print("init...")
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


