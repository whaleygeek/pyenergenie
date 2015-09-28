# monitor.py  27/09/2015  D.J.Whale
#
# Monitor settings of Energine MiHome plugs

import time
import pprint
from energenie import OpenHEMS, radio

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

class ENERGENIE():
    MFRID                            = 0x04
    PRODUCTID_C1_MONITOR             = 0x01
    PRODUCTID_R1_MONITOR_AND_CONTROL = 0x02
    CRYPT_PID                        = 242
    CRYPT_PIP                        = 0x0100


MONITOR_MESSAGE = {
    "header": {
        "mfrid":       ENERGENIE.MFRID,
        "productid":   ENERGENIE.PRODUCTID_C1_MONITOR,
        "encryptPIP":  ENERGENIE.CRYPT_PIP,
        "sensorid":    0xFFFFFF
    },
    "recs": [
        {
            "wr":      True,
            "paramid": OpenHEMS.PARAM_SWITCH_STATE,
            "typeid":  0x00,
            "length":  0x01,
            "value":   0x00
        }
    ]
}


def monitor():
    """Send monitor poke messages and capture any responses"""

    sendMonitorTimer = Timer(3)
    pollReceiveTimer = Timer(1)
    radio.receiver()

    while True:
        # See if there is a payload, and if there is, process it
        if pollReceiveTimer.check():
            if radio.isReceiveWaiting():
                trace("receiving payload")
                payload = radio.receive()
                decoded = OpenHEMS.decode(payload)
                pprint.pprint(decoded)

        # If it is time to send a monitor message, send it
        if sendMonitorTimer.check():
            trace("sending monitor message")
            payload = OpenHEMS.encode(MONITOR_MESSAGE)
            radio.transmitter()
            radio.transmit(payload)
            radio.receiver() # Keep in receiver mode as much as possible


if __name__ == "__main__":

    radio.init()
    OpenHEMS.init(ENERGENIE.CRYPT_PID)

    try:
        monitor()

    finally:
        radio.finished()

# END
