# energenie.py  24/05/2016  D.J.Whale
#
# Provides the app writer with a simple single module interface to everything.
# At the moment, this just hides the fact that the radio module needs to be initialised
# at the start and cleaned up at the end.
#
# Future versions of this *might* also start receive monitor or scheduler threads.

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

def init():
    """Start the Energenie system running"""
    radio.init()
    OpenThings.init(Devices.CRYPT_PID)


def finished():
    """Cleanly close the Energenie system when finished"""
    radio.finished()


# END