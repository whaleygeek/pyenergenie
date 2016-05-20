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

def log_method(m):
    def inner(*args, **kwargs):
        print("CALL %s with: %s %s" % (m, args, kwargs))
        r = m(*args, **kwargs)
        print("RETURN %s with: %s" % (m, r))
        return r
    return inner


class RegistryStore(): # This is data storage, so it it just the 'RegistRY'??
    """A mock in-memory only store, for testing and debugging"""
    def __init__(self, filename):
        self.filename = filename #TODO: Intentionally not used elsewhere
        self.store = {}

    #@log_method
    def __setitem__(self, key, value):
        self.store[key] = value

    #@log_method
    def __getitem__(self, key):
        return self.store[key]

    #@log_method
    def __delitem__(self, key):
        del self.store[key]

    #@log_method
    def keys(self):
        return self.store.keys()


class DeviceRegistry(): # this is actions, so is this the 'RegistRAR'??
    """A persistent registry for device class instance configurations"""
    def __init__(self, filename):
        self.store = RegistryStore(filename) # A dummy store, for testing

    @unimplemented
    def load(self):
        pass
        # load registry from disk/parse it

    @unimplemented
    def save(self):
        pass
        # persist registry to disk/write back new entries

    def add(self, device, name):
        """Add a device class instance to the registry, with a friendly name"""
        self.store[name] = device

    def get(self, name): # -> Device
        """Get the description for a device class from the store, and construct a class instance"""
        c = self.store[name]
        #TODO: Construct a new device class that is configured as per this data
        #for now, just return the RAM class instance as it is mocked

        #TODO: work out what type of device it is (fsk, ook)
        #TODO: decide which router to use for incoming messages
        #TODO: configure the message router so it will route to the device class instance for us
        #TODO: at what point is the payload decoded to get the address out?
        # OpenThings.decode() or TwoBit.decode() - where do those protocol handlers go in the pipeline?
        return c

    def delete(self, name):
        """Delete the named class instance"""
        del self.store[name]
        #TODO: delete from the RAM route too.

    def auto_create(self, context):
        """auto-create variables in the provided context, for all persisted registry entries"""
        if context == None:
            raise ValueError("Must provide a context to hold new variables")

        for name in self.store.keys():
            c = self.get(name) #TODO: should return an instantiated class
            # This creates a variable inside the context of this name, points to class instance
            setattr(context, name, c)

    def list(self):
        """List the registry in a vaguely printable format, mostly for debug"""
        for k in self.store.keys():
            print("DEVICE %s" % k)
            print("  %s" % self.store[k])


registry = DeviceRegistry("registry.txt")


# This will create all class instance variables in the module that imports the registry.
# So, if there is an entry called "tv" in the registry, then the app module
# will get a variable called tv that is bound to the appropriate device instance.
# You can then just say tv.turn_on() regardless of the type of device it is, as long
# as it has switching capability.
#
# usage:
#   import sys
#   from Registry import registry
#   registry.auto_create(sys.modules[__file__])


#----- DISCOVERY AND LEARNING -------------------------------------------------
#5. LEARN/DISCOVER: To be able to instigate and manage learn mode from within an app
#
#   a. To send specific commands to green button devices so they can
#      learn the pattern
#   ? broadcast specific (house_code, index) repeatedly
#   ? user assisted start/stop

#   b. To sniff for any messages from MiHome devices and capture them
#      for later analysis and turning into device objects
#   ? either as a special receive-only learn mode
#   ? or as part of normal receive operation through routing unknown device id's
#   ? need a way to take a device id and consult active directory list,
#     and route to the correct class instance - a router for incoming messages

#   This means we need an incoming message 'router' with a message pump
#   that the app can call - whenever it is in receive, does a peek and
#   if there is a message, it knows what modulaton scheme is in use
#   so can route the message with (modulation, payload)

#   c. To process MiHome join requests, and send MiHome join acks
#   ? this would be routed by address to the device class

#   This also needs the message pump


#----- MESSAGE ROUTER ---------------------------------------------------------

# a handler that is called whenever a message is received.
# routes it to the correct handling device class instance
# or instigates the unknown handler
# consults a RAM copy of part of the registry
# from mfrid,productid,sensorid -> handler

# The RAM copy is a routing table
# it must be updated whenever a factory returns a device class instance.

# Note, if you have a device class instance that is not registered,
# this means it cannot receive messages unless you pass them to it yourself.
# That's fine?

# might be one for OOK devices, a different one for FSK devices
# as they have different keying rules. OOK receive will only probably
# occur from another raspberry pi, or from a hand controller or MiHome hub.
# But it is possible to OOK receive a payload, it only has a house address
# and 4 index bits in it and no data, but those are routeable.

class Router():
    def __init__(self, name):
        self.name = name # probably FSK or OOK
        self.routes = {} # key(tuple of ids) -> value(device class instance)

    def add(self, address, instance):
        """Add this device instance to the routing table"""
        # When a message comes in for this address, it will be routed to its handle_message() method
        # address might be a string, a number, a tuple, but probably always the same for any one router
        self.routes[address] = instance

    def handle_message(self, payload):
        #TODO: decode address from payload
        #how do we do this?? Perhaps the protocol wrapper fsk or ook does it for us
        #as the message bubbles up out of the receiver?
        #e.g. OpenThigns.decode() would be applied to FSK incoming messages and build the header.
        #the 4bit.decode() could do the same for OOK incoming messages?
        #TODO: 4bit decoder needs a better name, it's really 2 bits per byte (1 bit per nibble)

        address = "TODO"
        #TODO: select handler
        if address in self.routes:
            ci = self.routes[address]
            #TODO check if it has a handle_message method, debug print if not?
            ci.handle_message(payload)

        else: # unknown address
            self.handle_unknown(address, payload)

    def handle_unknown(self, address, payload):
        #TODO: route to something that handles unknown addresses, e.g. discovery agent
        #discovery agent could be configured by overriding handle_unknown at construction time, below
        print("unknown address: %s" % address)
        print("ignored payload: %s" % payload)


fsk_router = Router("fsk")
ook_router = Router("ook")


#----- SIMPLE TEST HARNESS ----------------------------------------------------

def test_with_registry():
    #TODO need a way to separate device creation from device restoration
    #and the app needs to know what mode it is in.
    #creation is probably just a test feature, as a user would either
    #install the device, configure it, or learn it.


    # seed the registry
    registry.add(Devices.MIHO005(device_id=0x68b), "tv")
    registry.add(Devices.ENER002(device_id=(0xC8C8C, 1)), "fan")

    # test the auto create mechanism
    import sys
    registry.auto_create(sys.modules[__name__])

    # variables should now be created in module scope
    #print("tv %s" % tv)
    #print("fan %s" % fan)

    tv.turn_on()
    tv.turn_off()
    fan.turn_on()
    fan.turn_off()
    
    #print("tv switch:%s"  % tv.has_switch())
    #print("tv send:%s"    % tv.can_send())
    #print("tv receive:%s" % tv.can_receive())

    #print("fan switch:%s"  % fan.has_switch())
    #print("fan send:%s"    % fan.can_send())
    #print("fan receive:%s" % fan.can_receive())


if __name__ == "__main__":
    import OpenThings

    OpenThings.init(Devices.CRYPT_PID)
    test_with_registry()



# END
