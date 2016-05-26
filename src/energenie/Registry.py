# Registry.py  14/05/2016  D.J.Whale
#
# A simple registry of connected devices.
#
# NOTE: This is an initial, non persisted implementation only

from lifecycle import *

import time
try:
    # Python 2
    import Devices
    import OpenThings
except ImportError:
    # Python 3
    from . import Devices
    from . import OpenThings


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


#----- GENERIC KEY VALUE STORE ------------------------------------------------

class KVS():
    """A persistent key value store"""
    def __init__(self, filename=None):
        self.filename = filename
        self.store = {}

    @unimplemented
    def load(self, factory):
        """Load the whole file into an in-memory cache"""
        # The 'factory' is a place to go to turn device type names into actual class instances
        pass #TODO
        # open file for read
        # for each line read
        #   if in command mode
        #       if blank line, ignore it
        #       else not blank line
        #           split line, first word is command, second word is the key
        #           remember both
        #           change to data mode
        #   else in data mode
        #       if not blank line
        #           grab key=value
        #           add to temporary object
        #       else blank line
        #           process command,key,values
        # now eof
        #   process command,key,values, if it command is not empty
        # close file

    @unimplemented
    def process(self, command, key, values):
        """Process the temporary object"""
        pass #TODO
        # getattr method associated with the command name, error if no method
        # pass the key,values to that method to let it be processed

    @unimplemented
    def ADD(self, key, values):
        """Add a new item to the kvs"""
        # The ADD command process the next type= parameter as the class name in context
        # all other parameters are read as strings and passed to class constructor as kwargs
        pass #TODO
        # add key=values to the in memory object store
        # open file for append
        # write ADD command with key
        # for all keys in value
        #   write k=v
        # close file

    @unimplemented
    def IGN(self, key, values=None):
        """Ignore the whole record"""
        # The IGN command is the same length as ADD, allowing a seek/write to change any
        # command into IGN without changing the file size, effectively patching the file
        # so that the record is deleted.
        pass # There is nothing to do with this command

    @unimplemented
    def DEL(self, key, values=None):
        """Delete the key from the store"""
        # The DEL command deletes the rec from the store.
        # This is useful to build temporary objects and delete them later.
        # There is no need to write this to the file copy, we're processing the file
        pass #TODO
        # find key in object store, delete it

    @untested
    def __getitem__(self, key):
        return self.store[key]

    @untested
    def __setitem__(self, key, value):
        self.store[key] = value
        self.append(key, value)

    @untested
    def __delitem__(self, key):
        del self.store[key]
        self.remove(key)

    @untested
    def keys(self):
        return self.store.keys()

    @untested
    def size(self):
        return len(self.store)

    @untested
    def append(self, key, values):
        print("####HERE")
        print(values, type(values))
        """Append a new record to the persistent file"""
        with open(self.filename, 'w+') as f:
            f.write("ADD %s\n" % key)
            for k in values:
                v = values[k]
                f.write("%s=%s\n" % (k, v))
            f.write("\n")


    @unimplemented
    def remove(self, key):
        """Remove reference to this key in the file, and remove from in memory store"""
        pass #TODO
        # open file for read write
        # search line at a time, process each command
        #   when we find the command 'ADD key'
        #   reseek to start of line
        #   write overwrite ADD with IGN
        #   keep going in case of duplicates
        # close file

    @unimplemented
    def rewrite(self):
        """Rewrite the whole in memory cache over the top of the external file"""
        # useful if you have updated the in memory copy only and want to completely regenerate
        pass #TODO
        # create file new, for write only
        # for all objects in the store by key
        #   get value
        #   write ADD command key
        #   for all values
        #       write k=v
        #   write blank line
        # close file


#----- NEW DEVICE REGISTRY ----------------------------------------------------

# Done as a class, so we can have multiple registries if we want.

class DeviceRegistry(): # this is actions, so is this the 'RegistRAR'??
    """A persistent registry for device class instance configurations"""

    DEFAULT_FILENAME = "registry.kvs"

    def __init__(self, filename=None):
        if filename != None:
            self.store = KVS(filename)

    @untested
    def load_from(self, filename=None):
        """Start with a blank in memory registry, and load from the given filename"""
        if filename == None: filename = DeviceRegistry.DEFAULT_FILENAME
        # Create a new in memory store, effectively removing any existing in memory device class instances
        #TODO: Not good if there are routes to those class instances?
        self.store = KVS(filename) #TODO: later we might make it possible to load_from multiple files
        self.store.load(Devices.DeviceFactory)

    @unimplemented
    def reload(self):
        pass #TODO: reload from the persisted version
        #TODO: need to know what file it was previously loaded from
        #TODO: What about existing receive routes??

    @untested
    def rewrite(self):
        """Rewrite the persisted version from the in memory version"""
        self.store.rewrite()

    def load_into(self, context):
        """auto-create variables in the provided context, for all persisted registry entries"""
        if context == None:
            raise ValueError("Must provide a context to hold new variables")

        for name in self.store.keys():
            c = self.get(name)
            # This creates a variable inside the context of this name, points to class instance
            setattr(context, name, c)

    def add(self, device, name):
        """Add a device class instance to the registry, with a friendly name"""
        ####HERE
        #TODO: this is a Device class instance
        #need to get appropriate data out from it as a map
        #TODO: This is correct for a MiHomeDevice
        #but not for a LegacyDevice
        #TODO: Also, need the class name
        values = {
            "type":                Devices.MiHomeDevice, ##TODO MIHO005 ??
            "manufacturer_id":     device.manufacturer_id,
            "product_id":          device.product_id,
            "device_id":           device.device_id
        }
        self.store[name] = values

    def get(self, name): # -> Device
        """Get the description for a device class from the store, and construct a class instance"""
        c = self.store[name]

        #TODO: need to configure the correct router if device.can_receive()==True
        return c

    def delete(self, name):
        """Delete the named class instance"""
        del self.store[name]

    def list(self):
        """List the registry in a vaguely printable format, mostly for debug"""
        print("REGISTERED DEVICES:")
        for k in self.store.keys():
            print("  %s -> %s" % (k, self.store[k]))

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


registry = DeviceRegistry()
#TODO: registry.reload??


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

    def list(self):
        print("ROUTES:")
        for address in self.routes:
            print("  %s->%s" % (str(address), str(self.routes[address])))

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
        pass##print("message from unknown device:%s" % str(address))
        # default action is to drop message
        # override this method in sub classes if you want special processing

    def reject_device(self, address, message):
        pass##print("message rejected from:%s" % (str(address)))
        # default action is to drop message
        # override this method if you want special processing

    def accept_device(self, address, message, forward=True):
        ##print("accept_device:%s" % str(address))
        # At moment, intentionally assume everything is mfrid=Energenie
        product_id = address[1]
        device_id  = address[2]
        ##print("**** wiring up registry and router for %s" % str(address))
        ci = Devices.DeviceFactory.get_device_from_id(product_id, device_id)
        self.registry.add(ci, "auto_%s_%s" % (str(hex(product_id)), str(hex(device_id))))
        self.router.add(address, ci)

        # Finally, forward the first message to the new device class instance
        if forward:
            ##print("**** routing first message to class instance")
            ci.incoming_message(message)

        ##self.registry.list()
        ##self.router.list()
        return ci # The new device class instance that we created


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
        ##print("unknown device auto join %s" % str(address))

        #TODO: need to make this work with correct meta methods
        ##if not OpenThings.PARAM_JOIN in message:
        try:
            j = message[OpenThings.PARAM_JOIN]
        except KeyError:
            j = None

        if j == None: # not a join
            self.unknown_device(address, message)
        else: # it is a join
            # but don't forward the join request as it will be malformed with no value
            ci = self.accept_device(address, message, forward=False)
            ci.join_ack() # Ask new class instance to send a join_ack back to physical device


class JoinConfirmedDiscovery(Discovery):
    """A discovery agent that looks for join requests, and auto adds"""
    def __init__(self, registry, router, ask):
        Discovery.__init__(self, registry, router)
        self.ask_fn = ask

    def unknown_device(self, address, message):
        print("**** unknown device confirmed join %s" % str(address))

        #TODO: need to make this work with correct meta methods
        ##if not OpenThings.PARAM_JOIN in message:
        try:
            j = message[OpenThings.PARAM_JOIN]
        except KeyError:
            j = None

        if j == None: # not a join
            self.unknown_device(address, message)
        else: # it is a join
            y = self.ask_fn(address, message)
            if y:
                # but don't forward the join request as it will be malformed with no value
                ci = self.accept_device(address, message, forward=False)
                ci.join_ack() # Ask new class instance to send a join_ack back to physical device
            else:
                self.reject_device(address, message)


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

def discovery_none():
    fsk_router.when_unknown(None)

def discovery_auto():
    d = AutoDiscovery(registry, fsk_router)
    print("Using auto discovery")

def discovery_ask(ask_fn):
    d = ConfirmedDiscovery(registry, fsk_router, ask_fn)
    print("using confirmed discovery")

def discovery_autojoin():
    d = JoinAutoDiscovery(registry, fsk_router)
    print("using auto join discovery")

def discovery_askjoin(ask_fn):
    d = JoinConfirmedDiscovery(registry, fsk_router, ask_fn)
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
##discovery_none()
##discovery_auto()
##discovery_ask(ask)
discovery_autojoin()
##discovery_askjoin(ask)

# END
