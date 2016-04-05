# cleanup.py  05/04/2016  D.J.Whale
#
# Put all used GPIO pins into an input state
# Useful to recover from a crash

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.IN) # Green LED
GPIO.setup(22, GPIO.IN) # Red LED
GPIO.setup(7, GPIO.IN)  # CS
GPIO.setup(8, GPIO.IN)  # CS
GPIO.setup(11, GPIO.IN) # SCLK
GPIO.setup(10, GPIO.IN) # MOSI
GPIO.setup(9, GPIO.IN)  # MISO
GPIO.setup(25, GPIO.IN) # RESET

GPIO.cleanup()
