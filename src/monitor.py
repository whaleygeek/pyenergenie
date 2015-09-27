# monitor.py  27/09/2015  D.J.Whale
#
# Monitor settings of Energine MiHome plugs

import time
from energenie import radio, OpenHEMS

CRYPT_PID = 242
CRYPT_PIP = 0x0100

def trace(msg):
    print(str(msg))


#----- TIMER ------------------------------------------------------------------

class Timer():
    def __init__(self, ratesec=1):
        self.rate = ratesec
        self.nexttick = time.time()


    def check(self):
        """Maintain the timer and see if it is time for the next tick"""
        now = time.time()

        if now >= self.nexttick:
            # asynchronous tick, might drift, but won't stack up if late
            self.nexttick = now + self.rate
            return True

        return False


#----- TEST APPLICATION -------------------------------------------------------

def monitor():
    """Send monitor poke messages and capture any responses"""

    sendMonitorTimer = Timer(3)
    pollReceiveTimer = Timer(1)

    while True:
        # Keep in receiver mode as much as possible
        # but don't keep trying to switch into receiver if already there
        if radio.mode != "RECEIVER":
            radio.receiver()

        # See if there is a payload, and if there is, process it
        if pollReceiveTimer.check():
            if radio.isReceiveWaiting():
                trace("receiving payload")
                payload = radio.receive()
                trace("decoding payload")
                print(OpenHEMS.decode(payload))  # TODO decode from buffer to pydict

        # If it is time to send a monitor message, send it
        if sendMonitorTimer.check():
            trace("time for monitor")
            payload = OpenHEMS.make_monitor() # TODO encode from pydict to buffer
            radio.transmitter()
            trace("sending monitor message")
            radio.transmit(payload)


if __name__ == "__main__":

    radio.init()
    OpenHEMS.init(CRYPT_PID, CRYPT_PIP)

    try:
        monitor()

    finally:
        radio.finished()

# END
