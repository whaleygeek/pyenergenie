# Registry.py  14/05/2016  D.J.Whale
#
# A simple registry of connected devices.
#
# NOTE: This is an initial, non persisted implementation only

import time
try:
    import Devices # python 2
except ImportError:
    from . import Devices # python 3


def deprecated(m):
    print("warning: deprecated method %s" % str(m))
    return m


def unimplemented(m):
    print("warning: unimplemented method %s" % str(m))
    def inner(*args, **kwargs):
        print("warning: unimplemented method %s" % str(m))
        return m()
    return inner


def untested(m):
    print("warning: untested method %s" % str(m))
    return m


directory = {}

@deprecated
def allkeys(d):
    result = ""
    for k in d:
        if len(result) != 0:
            result += ','
        result += str(k)
    return result


@deprecated
def update(message):
    """Update the local directory with information about this device"""
    now      = time.time()
    header   = message["header"]
    sensorId = header["sensorid"]

    if not (sensorId in directory):
        # new device discovered
        desc = Devices.getDescription(header["mfrid"], header["productid"])
        print("ADD device:%s %s" % (hex(sensorId), desc))
        directory[sensorId] = {"header": message["header"]}
        #trace(allkeys(directory))

    directory[sensorId]["time"] = now
    #TODO would be good to keep recs, but need to iterate through all and key by paramid,
    #not as a list index, else merging will be hard.


@deprecated
def size():
    return len(directory)


@deprecated
def get_sensorids():
    return directory.keys()


@deprecated
def get_info(sensor_id):
    return directory[sensor_id]



#----- NEW DEVICE REGISTRY ----------------------------------------------------

# Done as a class, so we can have multiple registries if we want.

# TODO: file format? platform dependent database format, like dbm but there is
# a platform dependent one - but need the licence to be MIT so we can
# just embed it here to have zero dependencies.

# TODO: serialisation format for the individual device meta record? json?

class DeviceRegistry():
    pass

    @unimplemented
    def __init__(self, filename):
        pass
        # bind this object to a persisted file registry

    @unimplemented
    def load(self):
        pass
        # load registry from disk/parse it

    @unimplemented
    def save(self):
        pass
        # persist registry to disk/write back new entries

    @unimplemented
    def add(self, device, name):
        pass
        # add a device class instance to the registry with a friendly name

    @unimplemented
    def get(self, name): # -> Device
        pass
        # get a device by name from the registry
        # create a new device class instance from a name

    @unimplemented
    def delete(self, name):
        pass
        # delete a device from the registry

    @unimplemented
    def auto_create(self, context):
        pass
        # auto-create variables in a given scope, for all persisted registry entries

    @unimplemented
    def list(self):
        pass
        # list the registry in some printable format (like a configuration record)


registry = DeviceRegistry("registry.txt")

# This will create all class instance variables in the module that imports the registry.
# So, if there is an entry called "tv" in the registry, then the app module
# will get a variable called tv that is bound to the appropriate device instance.
# You can then just say tv.turn_on() regardless of the type of device it is, as long
# as it has switching capability.
#
# usage:
#   from Registry import registry
#   registry.auto_create(modules[__file__])

# END
