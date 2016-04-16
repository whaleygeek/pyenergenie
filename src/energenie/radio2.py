# radio2.py  15/04/2015  D.J.Whale
#
# New version of the radio driver, with most of the fast stuff pushed into C.
#
# This is a temporary test only, eventually when OOK and FSK are reimplemented
# and re-tested, this module will replace the radio.py/spi.py and spi_rpi.so files.

#NOTE 1: THIS IS A WORK IN PROGRESS - DO NOT USE
#It has the same interface as radio.py (intentionally)
#so that when it is finished, we can just exchange it and all should work
#as before, but faster and more reliably.

#NOTE 2: Also there is an idea to do a python wrapper, build the C code
#for an Arduino and wrap it with a simple serial message handler.
#This would then make it possible to use the Energenie Radio on a Mac/PC/Linux
#machine but by still using the same higher level Python code.
#All you would need is a different radio.py that marshalled data to and from
#the Arduino via pyserial.

LIBNAME = "radio_rpi.so"
#LIBNAME = "radio_mac.so" # testing

import ctypes
from os import path
mydir = path.dirname(path.abspath(__file__))

libradio                   = ctypes.cdll.LoadLibrary(mydir + "/" + LIBNAME)
radio_init_fn              = libradio["radio_init"]
radio_reset_fn             = libradio["radio_reset"]
radio_get_ver_fn           = libradio["radio_get_ver"]
radio_modulation_fn        = libradio["radio_modulation"]
radio_transmitter_fn       = libradio["radio_transmitter"]
radio_transmit_fn          = libradio["radio_transmit"]
radio_send_payload_fn      = libradio["radio_send_payload"]
#radio_receiver_fn          = libradio["radio_receiver"]
#radio_isReceiveWaiting_fn  = libradio["radio_isReceiveWaiting"]
#radio_receive_fn           = libradio["radio_receive"]
#radio_receive_payload_fn   = libradio["radio_receive_payload"]
radio_standby_fn           = libradio["radio_standby"]
radio_finished_fn          = libradio["radio_finished"]

RADIO_MODULATION_OOK = 0
RADIO_MODULATION_FSK = 1


def init():
    """Initialise the module ready for use"""
    #extern void radio_init(void);
    radio_init_fn()


def reset():
    """Reset the radio device"""
    #extern void radio_reset(void);
    radio_reset_fn()


def get_ver():
    """Read out the version number of the radio"""
    return radio_get_ver_fn()


def modulation(fsk=None, ook=None):
    """Switch modulation, if needed"""
    #extern void radio_modulation(RADIO_MODULATION mod);
    if ook:
        m = ctypes.c_int(RADIO_MODULATION_OOK)
    elif fsk:
        m = ctypes.c_int(RADIO_MODULATION_FSK)
    radio_modulation_fn(m)


def transmitter(fsk=None, ook=None):
    """Change into transmitter mode"""
    #extern void radio_transmitter(RADIO_MODULATION mod);
    if ook:
        m = ctypes.c_int(RADIO_MODULATION_OOK)
    elif fsk:
        m = ctypes.c_int(RADIO_MODULATION_FSK)
    radio_transmitter_fn(m)


def transmit(payload, times=1):
    """Transmit a single payload using the present modulation scheme"""
    #Note, this does a mode change before and after
    #extern void radio_transmit(uint8_t* payload, uint8_t len, uint8_t repeats);
    framelen = len(payload)
    Frame    = ctypes.c_ubyte * framelen
    txframe  = Frame(*payload)
    repeats  = ctypes.c_ubyte(times)
    radio_transmit_fn(txframe, framelen, repeats)


def send_payload(payload, times=1):
    """Transmit a payload in present modulation scheme, repeated"""
    #Note, this does not do a mode change before or after,
    #and assumes the mode is already transmit
    #extern void radio_send_payload(uint8_t* payload, uint8_t len, uint8_t repeats);

    framelen = len(payload)
    Frame    = ctypes.c_ubyte * framelen
    txframe  = Frame(*payload)
    repeats  = ctypes.c_ubyte(times)
    radio_send_payload_fn(txframe, framelen, repeats)


#def receiver(fsk=None, ook=None):
#    """Change into receiver mode"""
#    #extern void radio_receiver(RADIO_MODULATION mod);
#    if ook:
#        m = ctypes.c_int(RADIO_MODULATION_OOK)
#    elif fsk:
#        m = ctypes.c_int(RADIO_MODULATION_FSK)
#
#    radio_receiver_fn(m)


#def isReceiveWaiting():
#    """Check to see if a payload is waiting in the receive buffer"""
#    #extern RADIO_RESULT radio_isReceiveWaiting(void);
#    pass # TODO
#    # returns bool
#    ##res = radio_isReceiveWaitingFn()


#def receive():
#    """Put radio into receive mode and receive"""
#    #extern RADIO_RESULT radio_receive(uint8_t* buf, uint8_t len)
#    pass # TODO
#    ##radio_receive_fn(buf, len)
#    # returns list of bytes


#def radio_receive_payload():
#    """Receive a single payload"""
#    #extern RADIO_RESULT radio_receive_payload(uint8_t* buf, uint8_t len);
#    pass # TODO
#    ##radio_receive_payload_fn(buf, len)
#    # returns list of bytes


def standby():
    """Put radio into standby mode"""
    #extern void radio_standby(void);
    radio_standby_fn()


def finished():
    """Close the library down cleanly when finished"""
    #extern void radio_finished(void);
    radio_finished_fn()


# END
