# Timer.py  30/09/2015  D.J.Whale
#
# Simple cooperative timer services for repeating events

import time


#----- TIMER ------------------------------------------------------------------

class Timer():
    def __init__(self, ratesec=1, offsetsec=0):
        self.rate = ratesec
        self.nexttick = time.time() + offsetsec


    def check(self):
        """Maintain the timer and see if it is time for the next tick"""
        now = time.time()

        if now >= self.nexttick:
            # asynchronous tick, might drift, but won't stack up if late
            self.nexttick = now + self.rate
            return True

        return False

# END