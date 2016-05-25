# Registry.py  14/05/2016  D.J.Whale
#
# A simple registry of connected devices.
#
# NOTE: This is an initial, non persisted implementation only

from lifecycle import *

import time
try:
    import Devices # python 2
except ImportError:
    from . import Devices # python 3


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

    def size(self):
        return len(self.store)


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

    def size(self):
        """How many entries are there in the registry?"""
        return self.store.size()


    def devices(self):
        """Get a list of all device classes in the registry"""
        #TODO: Temporary method until we read up about iterable, so we can say
        # for devices in energenie.registry
        dl = []
        for k in self.store.keys():
            d = self.store[k]
            dl.append(d)
        return dl


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
        self.unknown_cb = None
        self.incoming_cb = None

    def add(self, address, instance):
        """Add this device instance to the routing table"""
        # When a message comes in for this address, it will be routed to its handle_message() method
        # address might be a string, a number, a tuple, but probably always the same for any one router
        self.routes[address] = instance

    def incoming_message(self, address, message):
        if self.incoming_cb != None:
            self.incoming_cb(address, message)

        if address in self.routes:
            ci = self.routes[address]
            ci.incoming_message(message)

        else: # unknown address
            self.handle_unknown(address, message)

    def when_incoming(self, callback):
        self.incoming_cb = callback

    def when_unknown(self, callback):
        """Register a callback for unknown messages"""
        #NOTE: this is the main hook point for auto discovery and registration
        self.unknown_cb = callback

    def handle_unknown(self, address, message):
        if self.unknown_cb != None:
            self.unknown_cb(address, message)
        else:
            # Default action is just a debug message, and drop the message
            print("Unknown address: %s" % str(address))


#---- DISCOVERY AGENT ---------------------------------------------------------
#
# Handles the discovery process when new devices appear and send reports.

class Discovery():
    """A Discovery agent that just reports any unknown devices"""
    def __init__(self, registry, router):
        self.registry = registry
        self.router   = router
        router.when_unknown(self.unknown_device)

    def unknown_device(self, address, message):
        print("message from unknown device:%s" % str(address))
        # default action is to drop message
        # override this method in sub classes if you want special processing

    def reject_device(self, address, message):
        print("message rejected from:%s" % (str(address)))
        # default action is to drop message
        # override this method if you want special processing

    def accept_device(self, address, message):
        print("TODO: accept_device:%s" % str(address))
        pass #TODO
        #    create device class instance from id information
        #    add to registry
        #    add to router
        #    forward message to new class instance for processing
        #TODO: return the new device class instance to caller


class AutoDiscovery(Discovery):
    """A discovery agent that auto adds unknown devices"""
    def __init__(self, registry, router):
        Discovery.__init__(self, registry, router)

    def unknown_device(self, address, message):
        self.accept_device(address, message)


class ConfirmedDiscovery(Discovery):
    """A discovery agent that asks the app before accepting/rejecting"""
    def __init__(self, registry, router, ask):
        Discovery.__init__(self, registry, router)
        self.ask_fn = ask

    def unknown_device(self, address, message):
        y = self.ask_fn(address, message)
        if y:
            self.accept_device(address, message)
        else:
            self.reject_device(address, message)


class JoinAutoDiscovery(Discovery):
    """A discovery agent that looks for join requests, and auto adds"""
    def __init__(self, registry, router):
        Discovery.__init__(self, registry, router)

    def unknown_device(self, address, message):
        print("TODO: unknown device auto join %s" % str(address))
        # if it is not a join req
        #   route to unhandled message handler
        # if it is a join req
        #   accept the device
        #   send join ack back to device (using new device class instance?)
        pass #TODO


class JoinConfirmedDiscovery(Discovery):
    """A discovery agent that looks for join requests, and auto adds"""
    def __init__(self, registry, router, ask):
        Discovery.__init__(self, registry, router)
        self.ask_fn = ask

    def unknown_device(self, address, message):
        print("TODO: unknown device confirmed join %s" % str(address))
        # if it is not a join req
        #   route to unhandled message handler
        # if it is a join req
        #     ask app
        #     if no
        #       reject device
        #     if yes
        #       accept device
        #       send join ack back to device (using new device class instance)
        pass #TODO




# Might rename these, especially when we add in other protocols
# such as devices that are 868 wirefree doorbells etc.

#TODO: Name is not completely representative of function.
# This is the Energenie 433.92MHz with OpenThings
fsk_router = Router("fsk")

#OOK receive not yet written
#It will be used to be able to learn codes from Energenie legacy hand remotes
##ook_router = Router("ook")


#TODO: Improve this interface
# (temporary) helpful methods to switch between different discovery methods
# Note that the __init__ automaticall registers itself with router

def discovery_auto():
    d = AutoDiscovery(registry, fsk_router)
    print("Using auto discovery")

def discovery_ask():
    d = ConfirmedDiscovery(registry, fsk_router)
    print("using confirmed discovery")

def discovery_autojoin():
    d = JoinAutoDiscovery(registry, fsk_router)
    print("using auto join discovery")

def discovery_askjoin():
    d = JoinConfirmedDiscovery(registry, fsk_router)
    print("using confirmed join discovery")


def ask(address, message):
    MSG = "Do you want to register to device: %s" % str(address)
    try:
        y = raw_input(MSG)
    except AttributeError:
        y = input(MSG)
    if y == "": return True
    y = y.upper()
    if y in ['Y', 'YES']: return True
    return False


# Default discovery mode, unless changed by app
discovery_auto()
##discovery_ask(ask)
##discovery_autojoin()
##discovery_askjoin(ask)

# END
