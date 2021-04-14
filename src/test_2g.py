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
OTHER = energenie.Devices.ENER002((0x123456, 4))

def do_left(f):
    """Put left side into a specific state"""
    print("LEFT:%d" % f)
    st = time.time()
    if f: LEFT.turn_on()
    else: LEFT.turn_off()
    et = time.time()
    print("burst time:%f" % (et-st))

def do_right(f):
    """Put right side into a specific state"""
    print("RIGHT:%d" % f)
    st = time.time()
    if f: RIGHT.turn_on()
    else: RIGHT.turn_off()
    et = time.time()
    print("burst time:%f" % (et-st))

def rnd_delay():
    """delay between 0 and N milliseconds randomly"""
    # This prevents the code syncing directly to the duty cycle of the
    # switch, and increases the chance of it missing the receive window.
    d = random.randint(0, RND_WINDOW_MS)
    d = float(d)/1000
    print("rnd_delay:%f" % d)
    time.sleep(d)

interferer_on = False
def interfere(delay):
    global interferer_on
    do_until = time.time() + delay
    time.sleep(0.5) # gap to allow OTHER to work
    while time.time() < do_until:
        if not interferer_on:
            print("OTHER on")
            OTHER.turn_on()
        else:
            print("OTHER off")
            OTHER.turn_off()
    interferer_on = not interferer_on


def cycle(delay):
    """"Do one cycle test of on/off of both switch sides"""
    do_left(1)
    interfere(delay)
    rnd_delay()
    do_right(1)
    interfere(delay)
    rnd_delay()

    do_left(0)
    interfere(delay)
    rnd_delay()
    do_right(0)
    interfere(delay)
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


