# energenie.py  24/05/2016  D.J.Whale
#
# Provides the app writer with a simple single module interface to everything.
# At the moment, this just hides the fact that the radio module needs to be initialised
# at the start and cleaned up at the end.
#
# Future versions of this *might* also start receive monitor or scheduler threads.

import time
import os
import sys

try:
    # Python 2
    import radio
    import Devices
    import Registry
    import OpenThings
except ImportError:
    # Python 3
    from . import radio
    from . import Devices
    from . import Registry
    from . import OpenThings


registry   = None
fsk_router = None
ook_router = None


def init():
    """Start the Energenie system running"""

    global registry, fsk_router, ook_router

    radio.init()
    OpenThings.init(Devices.CRYPT_PID)

    fsk_router = Registry.Router("fsk")

    #OOK receive not yet written
    #It will be used to be able to learn codes from Energenie legacy hand remotes
    ##ook_router = Registry.Router("ook")

    registry = Registry.DeviceRegistry()
    registry.set_fsk_router(fsk_router)
    ##registry.set_ook_router(ook_router

    path = os.path.join(sys.path[0], registry.DEFAULT_FILENAME)
    if os.path.isfile(path):
        registry.load_from(path)
        print("loaded registry from file")
        registry.list()
        fsk_router.list()

    # Default discovery mode, unless changed by app
    ##discovery_none()
    ##discovery_auto()
    ##discovery_ask(ask)
    discovery_autojoin()
    ##discovery_askjoin(ask)


def loop(receive_time=1):
    """Handle receive processing"""
    radio.receiver(fsk=True)
    timeout = time.time() + receive_time
    handled = False

    while True:
        if radio.is_receive_waiting():
            payload = radio.receive_cbp()
            now = time.time()
            try:
                msg        = OpenThings.decode(payload, receive_timestamp=now)
                hdr        = msg["header"]
                mfr_id     = hdr["mfrid"]
                product_id = hdr["productid"]
                device_id  = hdr["sensorid"]
                address    = (mfr_id, product_id, device_id)

                registry.fsk_router.incoming_message(address, msg)
                handled = True
            except OpenThings.OpenThingsException:
                print("Can't decode payload:%s" % payload)

        now = time.time()
        if now > timeout: break

    return handled


def finished():
    """Cleanly close the Energenie system when finished"""
    radio.finished()



def discovery_none():
    fsk_router.when_unknown(None)


def discovery_auto():
    d = Registry.AutoDiscovery(registry, fsk_router)
    ##print("Using auto discovery")


def discovery_ask(ask_fn):
    d = Registry.ConfirmedDiscovery(registry, fsk_router, ask_fn)
    ##print("using confirmed discovery")


def discovery_autojoin():
    d = Registry.JoinAutoDiscovery(registry, fsk_router)
    ##print("using auto join discovery")


def discovery_askjoin(ask_fn):
    d = Registry.JoinConfirmedDiscovery(registry, fsk_router, ask_fn)
    ##print("using confirmed join discovery")


def ask(address, message):
    MSG = "Do you want to register to device: %s? " % str(address)
    try:
        if message != None:
            print(message)
        y = raw_input(MSG)

    except AttributeError:
        y = input(MSG)

    if y == "": return True
    y = y.upper()
    if y in ['Y', 'YES']: return True
    return False


# END
