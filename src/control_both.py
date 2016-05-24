# control_both.py  15/05/2016  D.J.Whale
#
# A simple demo of combining both FSK (MiHome) and OOK (green button legacy)

import time
import energenie

GREEN_ID  = 1 # using default house code of 0x6C6C6
PURPLE_ID = 0x68b

green  = energenie.Devices.ENER002(GREEN_ID)
purple = energenie.Devices.MIHO005(PURPLE_ID)

def switch_loop():
    print("Turning green ON")
    green.turn_on()
    time.sleep(0.5)

    print("Turning purple ON")
    purple.turn_on()
    time.sleep(2)

    print("Turning green OFF")
    green.turn_off()
    time.sleep(0.5)

    print("Turning purple OFF")
    purple.turn_off()
    time.sleep(2)


if __name__ == "__main__":

    print("starting combined socket tester")
    energenie.init()

    try:
        while True:
            switch_loop()

    finally:
        energenie.finished()

# END
