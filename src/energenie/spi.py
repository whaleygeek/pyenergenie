# spi.py  19/07/2014  D.J.Whale
# 
# a C based SPI driver, with a python wrapper

LIBNAME = "spi_rpi.so"

import ctypes

from os import path
mydir = path.dirname(path.abspath(__file__))

libspi               = ctypes.cdll.LoadLibrary(mydir + "/" + LIBNAME)
spi_init_defaults_fn = libspi["spi_init_defaults"]
spi_init_fn          = libspi["spi_init"]
spi_select_fn        = libspi["spi_select"]
spi_deselect_fn      = libspi["spi_deselect"]
spi_byte_fn          = libspi["spi_byte"]
spi_frame_fn         = libspi["spi_frame"]
spi_finished_fn      = libspi["spi_finished"]

def trace(msg):
  pass #print("spi:" + msg)
  
def init_defaults():
  trace("calling init_defaults")
  spi_init_defaults_fn()
  
def init():
  trace("calling init")
  #TODO build a config structure
  #TODO pass in pointer to config structure
  #spi_init_fn()
  
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

