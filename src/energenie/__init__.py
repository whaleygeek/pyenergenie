# energenie.py  24/05/2016  D.J.Whale
#
# Provides the app writer with a simple single module interface to everything.
# At the moment, this just hides the fact that the radio module needs to be initialised
# at the start and cleaned up at the end.
#
# Future versions of this *might* also start receive monitor or scheduler threads.

import time

try:
    # Python 3
    from . import radio
    from . import Devices
    from . import Registry
    from . import OpenThings
except ImportError:
    # Python 2
    import radio
    import Devices
    import Registry
    import OpenThings

registry = Registry.registry
fsk_router = Registry.fsk_router

def init():
    """Start the Energenie system running"""
    radio.init()
    OpenThings.init(Devices.CRYPT_PID)


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

                Registry.fsk_router.handle_message(address, payload)
                handled = True
            except OpenThings.OpenThingsException:
                print("Can't decode payload:%s" % payload)

        now = time.time()
        if now > timeout: break

    return handled


def finished():
    """Cleanly close the Energenie system when finished"""
    radio.finished()


# END