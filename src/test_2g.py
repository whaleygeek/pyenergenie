import energenie
import time

BURST_SIZE = 5  # inner times * .027s (about 27ms per burst)
BURST_COUNT = 5  # outer times


class MYDEV(energenie.Devices.ENER002):
    def __init__(self, device_id, air_interface=None):
        energenie.Devices.ENER002.__init__(self, device_id, air_interface)
        self.radio_config.inner_times = BURST_SIZE
        self.radio_config.outer_times = BURST_COUNT

LEFT  = MYDEV((0x123456, 1))
RIGHT = MYDEV((0x123456, 2))

def do_left(f):
    print("LEFT:%d" % f)
    st = time.time()
    if f: LEFT.turn_on()
    else: LEFT.turn_off()
    et = time.time()
    print("burst time:%f" % (et-st))

def do_right(f):
    print("RIGHT:%d" % f)
    st = time.time()
    if f: RIGHT.turn_on()
    else: RIGHT.turn_off()
    et = time.time()
    print("burst time:%f" % (et-st))

def cycle(delay):
    do_left(1)
    time.sleep(delay)
    do_right(1)
    time.sleep(delay)

    do_left(0)
    time.sleep(delay)
    do_right(0)
    time.sleep(delay)

print("init...")
energenie.init()
print("done")

try:
    while True:
        cycle(4)

finally:
    print("cleanup...")
    energenie.finished()
    print("done")

