# spi.py  19/07/2014  D.J.Whale
# 
# a C based SPI driver, with a python wrapper

LIBNAME = "spi_rpi.so"

import ctypes
import time

from os import path
mydir = path.dirname(path.abspath(__file__))

RESET     = 25 # BCM GPIO
LED_GREEN = 27 # BCM GPIO (not B rev1)
LED_RED   = 22 # BCM GPIO

libspi               = ctypes.cdll.LoadLibrary(mydir + "/" + LIBNAME)
spi_init_defaults_fn = libspi["spi_init_defaults"]
spi_init_fn          = libspi["spi_init"]
spi_select_fn        = libspi["spi_select"]
spi_deselect_fn      = libspi["spi_deselect"]
spi_byte_fn          = libspi["spi_byte"]
spi_frame_fn         = libspi["spi_frame"]
spi_finished_fn      = libspi["spi_finished"]

# Might put this in a separate rpi_gpio.so and dynamically link both
# from rpi_spi and from python, but have to be careful with sharing
# memmap. For now, we only use this to control the radio RESET,
# so let's leave this embedded inside the rpi_spi.so until we
# need any more visibility
#gpio_init_fn            = libspi["gpio_init"]
#gpio_setin_fn           = libspi["gpio_setin"]
gpio_setout_fn          = libspi["gpio_setout"]
gpio_high_fn            = libspi["gpio_high"]
gpio_low_fn             = libspi["gpio_low"]
#gpio_write_fn           = libspi["gpio_write"]
#gpio_read_fn            = libspi["gpio_read"]


def trace(msg):
  pass #print("spi:" + msg)


# Note, this is radio specific, not SPI specific. hmm.
# fine for now to test the theory, but architecturally this is wrong.
# might have an optional reset line in spi_config, and an spi_reset()
# in spi.c that excercises it if required, as a more generic way
# to do this, as most SPI devices have a reset line. If value not
# defined, nothing happens. If value defined, it must have a
# polarity too, and spi.c will set it to an output inactive
# until reset is required. Also need to set up a reset active
# time and a 'after reset' guard time. That will cover most
# cases generically without having to surface the whole inner GPIO
# out to the python.

def reset():
  trace("reset")

  reset = ctypes.c_int(RESET)
  gpio_setout_fn(reset)
  gpio_high_fn(reset)
  time.sleep(0.1)
  gpio_low_fn(reset)
  time.sleep(0.1)

  # Put LEDs into known off state
  led_red = ctypes.c_int(LED_RED)
  led_green = ctypes.c_int(LED_GREEN)
  gpio_setout_fn(led_red)
  gpio_low_fn(led_red)
  gpio_setout_fn(led_green)
  gpio_low_fn(led_green)


def init_defaults():
  trace("calling init_defaults")
  spi_init_defaults_fn()


def init():
  trace("calling init")
  #TODO build a config structure
  #TODO pass in pointer to config structure
  #spi_init_fn()


def start_transaction():
  """Start a transmit or receive, perhaps multiple bursts"""
  # turn the GREEN LED on
  led_green = ctypes.c_int(LED_GREEN)
  gpio_high_fn(led_green)


def end_transaction():
  """End a transmit or receive, perhaps multiple listens"""
  # turn the GREEN LED off
  led_green = ctypes.c_int(LED_GREEN)
  gpio_low_fn(led_green)


def select():
  trace("calling select")
  spi_select_fn()


def deselect():
  trace("calling deselect")
  spi_deselect_fn()


def byte(tx):
  txbyte = ctypes.c_ubyte(tx)
  #trace("calling byte")
  rxbyte = spi_byte_fn(txbyte)
  return rxbyte

  
def frame(txlist):
  trace("calling frame ")
  framelen = len(txlist)
  #print("len:" + str(framelen))
  Frame = ctypes.c_ubyte * framelen
  txframe = Frame(*txlist)
  rxframe = Frame()
  
  spi_frame_fn(ctypes.byref(txframe), ctypes.byref(rxframe), framelen)
  rxlist = []
  for i in range(framelen):
    rxlist.append(rxframe[i])
  return rxlist


def finished():
  trace("calling finished")
  spi_finished_fn()


# END


