# test_2g.py  29/03/21  D.J.Whale
#
# cycle test the 2-gang light switch timing
# The purpose of this is to characterise the required burst length
# and holdoff time between messages, as the 2-gang device is a
# bit fussy with its timing.

import energenie
import time
import random

BURST_SIZE = 22  # inner times * .027s (about 27ms per burst)
BURST_COUNT = 2  # outer times
HOLDOFF = 3
RND_WINDOW_MS = 100

class MYDEV(energenie.Devices.ENER002):
    """Customised legacy device with overriden burst timing"""
    def __init__(self, device_id, air_interface=None):
        energenie.Devices.ENER002.__init__(self, device_id, air_interface)
        self.radio_config.inner_times = BURST_SIZE
        self.radio_config.outer_times = BURST_COUNT

LEFT  = MYDEV((0x123456, 1))
RIGHT = MYDEV((0x123456, 2))

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

def cycle(delay):
    """"Do one cycle test of on/off of both switch sides"""
    do_left(1)
    time.sleep(delay)
    rnd_delay()
    do_right(1)
    time.sleep(delay)
    rnd_delay()

    do_left(0)
    time.sleep(delay)
    rnd_delay()
    do_right(0)
    time.sleep(delay)
    rnd_delay()

def test_loop():
    print("init...")
    energenie.init()
    print("done")

    try:
        while True:
            cycle(HOLDOFF)

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
    test_loop()


