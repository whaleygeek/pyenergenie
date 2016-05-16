# radio2.py  15/04/2015  D.J.Whale
#
# New version of the radio driver, with most of the fast stuff pushed into C.
#
# NOTE 1: This is only used for OOK transmit & FSK transmit at the moment.
# FSK receive is currently being re-implemented in radio.c

# NOTE 2: Also there is an idea to do a python wrapper, build the C code
# for an Arduino and wrap it with a simple serial message handler.
# This would then make it possible to use the Energenie Radio on a Mac/PC/Linux
# machine but by still using the same higher level Python code.
# All you would need is a different radio.py that marshalled data to and from
# the Arduino via pyserial.

#TODO: Should really add parameter validation here, so that C code doesn't have to.
#although it will be faster in C (C could be made optional, like an assert?)

LIBNAME = "drv/radio_rpi.so"
##LIBNAME = "drv/radio_mac.so" # testing

import time
import ctypes
from os import path
mydir = path.dirname(path.abspath(__file__))

libradio                     = ctypes.cdll.LoadLibrary(mydir + "/" + LIBNAME)
radio_init_fn                = libradio["radio_init"]
radio_reset_fn               = libradio["radio_reset"]
radio_get_ver_fn             = libradio["radio_get_ver"]
radio_modulation_fn          = libradio["radio_modulation"]
radio_transmitter_fn         = libradio["radio_transmitter"]
radio_transmit_fn            = libradio["radio_transmit"]
radio_send_payload_fn        = libradio["radio_send_payload"]
radio_receiver_fn            = libradio["radio_receiver"]
radio_is_receive_waiting_fn  = libradio["radio_is_receive_waiting"]
radio_get_payload_len_fn     = libradio["radio_get_payload_len"]
radio_get_payload_cbp_fn     = libradio["radio_get_payload_cbp"]
radio_standby_fn             = libradio["radio_standby"]
radio_finished_fn            = libradio["radio_finished"]

RADIO_MODULATION_OOK = 0
RADIO_MODULATION_FSK = 1

# A temporary limit, the receiver will only receive 1 FIFO worth of data maximul
# This includes the length byte at the start of an OpenThings message
MAX_RX_SIZE = 66


#TODO RADIO_RESULT_XX

def trace(msg):
    print(str(msg))


def tohex(l):
    line = ""
    for item in l:
        line += hex(item) + " "
    return line


def unimplemented(m):
    print("warning: method is not implemented:%s" % m)
    return m


def deprecated(m):
    """Load-time warning about deprecated method"""
    print("warning: method is deprecated:%s" % m)
    return m


def untested(m):
    """Load-time warning about untested function"""
    print("warning: method is untested:%s" % m)
    return m


def disabled(m):
    """Load-time waring about disabled function"""
    print("warning: method is disabled:%s" % m)
    def nothing(*args, **kwargs):pass
    return nothing


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
    else:
        raise RuntimeError("Must choose fsk or ook mode")
    radio_modulation_fn(m)


def transmitter(fsk=None, ook=None):
    """Change into transmitter mode"""
    #extern void radio_transmitter(RADIO_MODULATION mod);
    if ook:
        m = ctypes.c_int(RADIO_MODULATION_OOK)
    elif fsk:
        m = ctypes.c_int(RADIO_MODULATION_FSK)
    else: # defaults to FSK
        m = ctypes.c_int(RADIO_MODULATION_FSK)
    radio_transmitter_fn(m)


def transmit(payload, outer_times=1, inner_times=8, outer_delay=0):
    """Transmit a single payload using the present modulation scheme"""
    #Note, this optionally does a mode change before and after
    #extern void radio_transmit(uint8_t* payload, uint8_t len, uint8_t repeats);

    framelen = len(payload)
    if framelen < 1 or framelen > 255:
        raise ValueError("frame len must be 1..255")
    if outer_times < 1:
        raise ValueError("outer_times must be >0")
    if inner_times < 1 or inner_times > 255:
        raise ValueError("tx times must be 0..255")

    framelen     = len(payload)
    Frame        = ctypes.c_ubyte * framelen
    txframe      = Frame(*payload)
    inner_times  = ctypes.c_ubyte(inner_times)
    
    for i in range(outer_times):
        #TODO: transmit() will mode change if required
        #this means that outer_times will keep popping and pushing the mode
        #that might be ok, as it will force all the flags to clear?
        radio_transmit_fn(txframe, framelen, inner_times)
        if outer_delay != 0:
            time.sleep(outer_delay)


def send_payload(payload, outer_times=1, inner_times=8, outer_delay=0):
    """Transmit a payload in present modulation scheme, repeated"""
    #Note, this does not do a mode change before or after,
    #and assumes the mode is already transmit
    #extern void radio_send_payload(uint8_t* payload, uint8_t len, uint8_t times);

    framelen = len(payload)
    if framelen < 1 or framelen > 255:
        raise ValueError("frame len must be 1..255")
    if outer_times < 1:
        raise ValueError("outer_times must be >0")
    if inner_times < 1 or inner_times > 255:
        raise ValueError("tx times must be 0..255")
    Frame          = ctypes.c_ubyte * framelen
    txframe        = Frame(*payload)
    inner_times    = ctypes.c_ubyte(inner_times)

    for i in range(outer_times):
        radio_send_payload_fn(txframe, framelen, inner_times)
        if outer_delay != 0:
            time.sleep(outer_delay)


def receiver(fsk=None, ook=None):
    """Change into receiver mode"""
    #extern void radio_receiver(RADIO_MODULATION mod);
    if ook:
        m = ctypes.c_int(RADIO_MODULATION_OOK)
    elif fsk:
        m = ctypes.c_int(RADIO_MODULATION_FSK)
    else: # defaults to FSK
        m = ctypes.c_int(RADIO_MODULATION_FSK)

    radio_receiver_fn(m)


def is_receive_waiting():
    """Check to see if a payload is waiting in the receive buffer"""
    #extern RADIO_RESULT radio_is_receive_waiting(void);
    res = radio_is_receive_waiting_fn()
    # this is RADIO_RESULT_OK_TRUE or RADIO_RESULT_OK_FALSE
    # so it is safe to evaluate it as a boolean number.
    return (res != 0)


def receive(size=None):
    """Receive a single payload"""

    if size == None:
        return receive_cbp()
    else:
        return receive_len(size)


def receive_cbp():
    """Receive a count byte preceded payload"""
    ##trace("receive_cbp")

    ##bufsize = MAX_RX_SIZE
    bufsize = 255 # testing
    Buffer = ctypes.c_ubyte * bufsize
    rxbuf  = Buffer()
    buflen = ctypes.c_ubyte(bufsize)
    #RADIO_RESULT radio_get_payload_cbp(uint8_t* buf, uint8_t buflen)

    result = radio_get_payload_cbp_fn(rxbuf, buflen)

    if result != 0: # RADIO_RESULT_OK
        raise RuntimeError("Receive failed, radio.c error code %s" % hex(result))

    size = 1+rxbuf[0] # The count byte in the payload

    # turn buffer into a list of bytes, using 'size' as the counter
    rxlist = []
    for i in range(size):
        rxlist.append(rxbuf[i])

    ##trace("receive_cbp returhs %s" % tohex(rxlist))
    return rxlist # Python len(rxlist) tells us how many bytes including length byte if present


@untested
def receive_len(size):
    """Receive a fixed payload size"""

    bufsize = size

    Buffer = ctypes.c_ubyte * bufsize
    rxbuf  = Buffer()
    buflen = ctypes.c_ubyte(bufsize)
    #RADIO_RESULT radio_get_payload_len(uint8_t* buf, uint8_t buflen)

    result = radio_get_payload_len_fn(rxbuf, buflen)

    if result != 0: # RADIO_RESULT_OK
        raise RuntimeError("Receive failed, error code %s" % hex(result))

    # turn buffer into a list of bytes, using 'size' as the counter
    rxlist = []
    for i in range(size):
        rxlist.append(rxbuf[i])

    return rxlist # Python len(rxlist) tells us how many bytes including length byte if present


def standby():
    """Put radio into standby mode"""
    #extern void radio_standby(void);
    radio_standby_fn()


def finished():
    """Close the library down cleanly when finished"""
    #extern void radio_finished(void);
    radio_finished_fn()


# END
