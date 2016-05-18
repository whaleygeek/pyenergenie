# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices
# This table is mostly reverse-engineered from various websites and web catalogues.

MFRID_ENERGENIE                  = 0x04
MFRID                            = MFRID_ENERGENIE


#PRODUCTID_MIHO001               =        #         Home Hub
#PRODUCTID_MIHO002               =        #         Control only (Uses Legacy OOK protocol)
#PRODUCTID_MIHO003               = 0x0?   #         Hand Controller
PRODUCTID_MIHO004                = 0x01   #         Monitor only
PRODUCTID_MIHO005                = 0x02   #         Adaptor Plus
PRODUCTID_MIHO006                = 0x05   #         House Monitor
#PRODUCTID_MIHO007               = 0x0?   #         Double Wall Socket White
#PRODUCTID_MIHO008               = 0x0?   #         Single light switch
#PRODUCTID_MIHO009 not used
#PRODUCTID_MIHO010 not used
#PRODUCTID_MIHO011 not used
#PRODUCTID_MIHO012 not used
PRODUCTID_MIHO013                = 0x03   #         eTRV
#PRODUCTID_MIHO014               = 0x0?   #         In-line Relay
#PRODUCTID_MIHO015 not used
#PRODUCTID_MIHO016 not used
#PRODUCTID_MIHO017
#PRODUCTID_MIHO018
#PRODUCTID_MIHO019
#PRODUCTID_MIHO020
#PRODUCTID_MIHO021               = 0x0?   #         Double Wall Socket Nickel
#PRODUCTID_MIHO022               = 0x0?   #         Double Wall Socket Chrome
#PRODUCTID_MIHO023               = 0x0?   #         Double Wall Socket Brushed Steel
#PRODUCTID_MIHO024               = 0x0?   #         Style Light Nickel
#PRODUCTID_MIHO025               = 0x0?   #         Style Light Chrome
#PRODUCTID_MIHO026               = 0x0?   #         Style Light Steel
#PRODUCTID_MIHO027 starter pack bundle
#PRODUCTID_MIHO028 eco starter pack
#PRODUCTID_MIHO029 heating bundle
#PRODUCTID_MIHO030 not used
#PRODUCTID_MIHO031 not used
#PRODUCTID_MIHO032 not used
#PRODUCTID_MIHO033 not used
#PRODUCTID_MIHO034 not used
#PRODUCTID_MIHO035 not used
#PRODUCTID_MIHO036 not used
#PRODUCTID_MIHO037 Adaptor Plus Bundle
#PRODUCTID_MIHO038 2-gang socket Bundle
#PRODUCTID_MIHO039 2-gang socket Bundle black nickel
#PRODUCTID_MIHO040 2-gang socket Bundle chrome
#PRODUCTID_MIHO041 2-gang socket Bundle stainless steel

# Default keys for OpenThings encryption and decryption
CRYPT_PID                        = 242
CRYPT_PIP                        = 0x0100

# OpenThings does not support a broadcast id,
# but Energenie added one for their MiHome Adaptors.
# This makes simple discovery possible.
BROADCAST_ID                     = 0xFFFFFF # Energenie broadcast

#TODO: This might be deprecated now, and replaced with the DeviceFactory?
def getDescription(mfrid, productid):
    if mfrid == MFRID_ENERGENIE:
        mfr = "Energenie"
        if productid == PRODUCTID_MIHO004:
            product = "MIHO004 MONITOR"
        elif productid == PRODUCTID_MIHO005:
            product = "MIHO005 ADAPTOR PLUS"
        elif productid == PRODUCTID_MIHO006:
            product = "MIHO006 HOUSE MONITOR"
        elif productid == PRODUCTID_MIHO013:
            product = "MIHO013 ETRV"
        else:
            product = "UNKNOWN_%s" % str(hex(productid))
    else:
        mfr     = "UNKNOWN_%s" % str(hex(mfrid))
        product = "UNKNOWN_%s" % str(hex(productid))

    return "Manufacturer:%s Product:%s" % (mfr, product)


#TODO this might be deprecated now, and replaced with the Device classes.
#e.g. if there is a turn_on method or get_switch method, it has a switch.
def hasSwitch(mfrid, productid):
    if mfrid != MFRID:                  return False
    if productid == PRODUCTID_MIHO005:  return True
    return False


#----- CONTRACT WITH AIR-INTERFACE --------------------------------------------

# this might be a real air_interface (a radio), or an adaptor interface
# (a message scheduler with a queue).
#
# TODO: As such, we need to handle:
#   synchronous send
#   synchronous receive
#   asynchronous send (deferred)
#   asynchronous receive (deferred)

# air_interface has:
#   configure(parameters)
#   send(payload)
#   send(payload, parameters)
#   listen(parameters)
#   check() -> payload or None


#----- NEW DEVICE CLASSES -----------------------------------------------------

class Device():
    """A generic connected device abstraction"""
    def __init__(self, air_interface):
        self.air_interface = air_interface
        class Config(): pass
        self.config = Config()

    def has_switch(self):
        return False

    def can_send(self):
        return False

    def can_receive(self):
        return False

    def get_radio_config(self):
        return self.config

    def get_last_receive_time(self): # ->timestamp
        """The timestamp of the last time any message was received by this device"""
        return self.last_receive_time

    def get_next_receive_time(self): # -> timestamp
        """An estimate of the next time we expect a message from this device"""
        pass

    def incoming_message(self, payload):
        # incoming_message (OOK or OpenThings as appropriate, stripped of header? decrypted, decoded to pydict)
        # default action of base class is to just print the payload
        print("incoming:%s" % payload)

    def send_message(self, payload):
        print("send_message %s" % payload)

    def __repr__(self):
        return "Device()"


class EnergenieDevice(Device):
    """An abstraction for any kind of Energenie connected device"""
    def __init__(self, air_interface, device_id=None):
        Device.__init__(self, air_interface)
        self.device_id = device_id

    def get_device_id(self): # -> id:int
        return self.device_id

    def __repr__(self):
        return "Device(%s)" % str(self.device_id)


class LegacyDevice(EnergenieDevice):
    """An abstraction for Energenie green button legacy OOK devices"""
    def __init__(self, air_interface):
        EnergenieDevice.__init__(self, air_interface)
        self.config.frequency  = 433.92
        self.config.modulation = "OOK"
        self.config.codec      = "4bit"

    def __repr__(self):
        return "LegacyDevice(%s)" % str(self.device_id)

    def send_message(self, payload):
        if self.air_interface != None:
            #TODO: might want to send the config, either as a send parameter,
            #or by calling air_interface.configure() first?
            self.air_interface.send(payload)
        else:
            d = self.device_id #TODO: Not part of Device now
            print("send_message(mock[%s]):%s" % (str(d), payload))



class MiHomeDevice(EnergenieDevice):
    """An abstraction for Energenie new style MiHome FSK devices"""
    def __init__(self, air_interface, device_id=None):
        EnergenieDevice.__init__(self, air_interface, device_id)
        self.config.frequency  = 433.92
        self.config.modulation = "FSK"
        self.config.codec      = "OpenThings"
        self.manufacturer_id   = MFRID_ENERGENIE
        self.product_id        = None

        #Different devices might have different PIP's
        #if we are cycling codes on each message?
        #self.config.encryptPID = CRYPT_PID
        #self.config.encryptPIP = CRYPT_PIP

    def __repr__(self):
        return "MiHomeDevice(%s,%s,%s)" % (str(self.manufacturer_id), str(self.product_id), str(self.device_id))

    def get_manufacturer_id(self): # -> id:int
        return self.manufacturer_id

    def get_product_id(self): # -> id:int
        return self.product_id

    def send_message(self, payload):
        if self.air_interface != None:
            #TODO: might want to send the config, either as a send parameter,
            #or by calling air_interface.configure() first?
            self.air_interface.send(payload)
        else:
            m = self.manufacturer_id #TODO: Not part of Device now
            p = self.product_id #TODO: Not part of Device now
            d = self.device_id #TODO: Not part of Device now
            print("send_message(mock[%s %s %s]):%s" % (str(m), str(p), str(d), payload))



class ENER002(LegacyDevice):
    """A green-button switch"""
    def __init__(self, air_interface=None, device_id=None):
        LegacyDevice.__init__(self, air_interface)
        #NOTE: tuple of (house_address, device_index)
        self.device_id = device_id
        self.config.tx_repeats = 8
        #no productid code for legacy devices?

    def can_send(self):
        return True

    def has_switch(self):
        return True

    def turn_on(self):
        pass # TODO
        self.send_message("turn on") # TODO

    def turn_off(self):
        pass # TODO
        self.send_message("turn off") # TODO


class MIHO005(MiHomeDevice):
    """An Energenie MiHome Adaptor Plus"""
    def __init__(self, air_interface=None, device_id=None):
        MiHomeDevice.__init__(self, air_interface)
        self.product_id = PRODUCTID_MIHO005
        self.device_id  = device_id
        class Readings():
            switch         = None
            voltage        = None
            frequency      = None
            apparent_power = None
            reactive_power = None
            real_power     = None
        self.readings = Readings()
        self.config.tx_repeats = 4

    def can_send(self):
        return True

    def can_receive(self):
        return True

    def has_switch(self):
        return True

    def get_readings(self): # -> readings:pydict
        """A way to get all readings as a single consistent set"""
        return self.readings

    def turn_on(self):
        #TODO: build header
        #TODO: add rec SWITCH=1
        #TODO: self.send_message()
        self.send_message("turn on") # TODO

    def turn_off(self):
        #TODO: build header
        #TODO: add rec SWITCH=0
        #TODO: self.send_message(OPENTHINGS_SWITCH_MESSAGE, False)
        self.send_message("turn off") # TODO

    #TODO: difference between 'is on and 'is requested on'
    #TODO: difference between 'is off' and 'is requested off'
    #TODO: switch state might be 'unknown' if not heard.
    #TODO: switch state might be 'turning_on' or 'turning_off' if send request and not heard response yet

    def is_on(self): # -> boolean
        """True, False, or None if unknown"""
        s = self.get_switch()
        if s == None: return None
        return s

    def is_off(self): # -> boolean
        """True, False, or None if unknown"""
        s = self.get_switch()
        if s == None: return None
        return not s

    def get_switch(self): # -> boolean
        """Last stored state of the switch, might be None if unknown"""
        return self.readings.switch

    def get_voltage(self): # -> voltage:float
        """Last stored state of voltage reading, None if unknown"""
        return self.readings.voltage

    def get_frequency(self): # -> frequency:float
        """Last stored state of frequency reading, None if unknown"""
        return self.readings.frequency

    def get_apparent_power(self): # ->power:float
        """Last stored state of apparent power reading, None if unknown"""
        return self.readings.apparent_power

    def get_reactive_power(self): # -> power:float
        """Last stored state of reactive power reading, None if unknown"""
        return self.readings.reactive_power

    def get_real_power(self): #-> power:float
        """Last stored state of real power reading, None if unknown"""
        return self.readings.real_power


class MIHO006(MiHomeDevice):
    """An Energenie MiHome Home Monitor"""
    def __init__(self, air_interface=None, device_id=None):
        MiHomeDevice.__init__(self, air_interface)
        self.product_id = PRODUCTID_MIHO006
        self.device_id  = device_id
        class Readings():
            battery_voltage = None
            current         = None
        self.readings = Readings()

    def can_send(self):
        return True

    def get_battery_voltage(self): # -> voltage:float
        return self.readings.battery_voltage

    def get_current(self): # -> current:float
        return self.readings.current


class MIHO013(MiHomeDevice):
    """An Energenie MiHome eTRV Radiator Valve"""
    def __init__(self, air_interface=None, device_id=None):
        MiHomeDevice.__init__(self, air_interface)
        self.product_id = PRODUCTID_MIHO013
        self.device_id  = device_id
        class Readings():
            battery_voltage      = None
            ambient_temperature  = None
            pipe_temperature     = None
            setpoint_temperature = None
            valve_position       = None
        self.readings = Readings()
        self.config.tx_repeats = 10

    def can_send(self):
        return True

    def can_receive(self):
        return True

    def get_battery_voltage(self): # ->voltage:float
        return self.readings.battery_voltage

    def get_ambient_temperature(self): # -> temperature:float
        return self.readings.ambient_temperature

    def get_pipe_temperature(self): # -> temperature:float
        return self.readings.pipe_temperature

    def get_setpoint_temperature(self): #-> temperature:float
        return self.readings.setpoint_temperature

    def set_setpoint_temperature(self, temperature):
        pass # TODO command
        self.send_message("set setpoint temp") # TODO

    def get_valve_position(self): # -> position:int?
        pass # TODO

    def set_valve_position(self, position):
        pass # TODO command
        self.send_message("set valve pos") #TODO

    #TODO: difference between 'is on and 'is requested on'
    #TODO: difference between 'is off' and 'is requested off'
    #TODO: switch state might be 'unknown' if not heard.
    #TODO: switch state might be 'turning_on' or 'turning_off' if send request and not heard response yet

    def turn_on(self): # command
        pass # TODO command i.e. valve position?
        self.send_message("turn on") #TODO

    def turn_off(self): # command
        pass # TODO command i.e. valve position?
        self.send_message("turn off") #TODO

    def is_on(self): # query last known reported state (unknown if changing?)
        pass # TODO i.e valve is not completely closed?

    def is_off(self): # query last known reported state (unknown if changing?)
        pass # TODO i.e. valve is completely closed?


#----- DEVICE FACTORY ---------------------------------------------------------

# This is a singleton, but might not be in the future.
# i.e. we might have device factories for lots of different devices.
# and a DeviceFactory could auto configure it's set of devices
# with a specific air_interface for us.
# i.e. this might be the EnergenieDeviceFactory, there might be others

class DeviceFactory():
    """A place to come to, to get instances of device classes"""
    devices = {
        # official name            friendly name
        "ENER002":     ENER002,    "GreenButton": ENER002,
        "MIHO005":     MIHO005,    "AdaptorPlus": MIHO005,
        "MIHO006":     MIHO006,    "HomeMonitor": MIHO006,
        "MIHO013":     MIHO013,    "eTRV":        MIHO013,
    }
    default_air_interface = None

    @staticmethod
    def set_default_air_interface(air_interface):
        DeviceFactory.default_air_interface = air_interface

    @staticmethod
    def keys():
        return DeviceFactory.devices.keys()

    @staticmethod
    def get_device(name, air_interface=None, device_id=None):
        """Get a device by name, construct a new instance"""
        if not name in DeviceFactory.devices:
            raise ValueError("Unsupported device:%s" % name)

        c = DeviceFactory.devices[name]
        if air_interface == None:
            air_interface = DeviceFactory.default_air_interface
        return c(air_interface, device_id)


#----- TEMPORARY TEST HARNESS -------------------------------------------------

#hmm: need two addresses for legacy - use a tuple (house_address, index)

#unless we have an adaptor class for air_interface which represents the
#collective house address for a house code. So if you use more than one
#house address, you create multiple air interface adaptors with different
#house codes, that just delegate to the same actual radio air interface?
#bit like a little local router?

#legacy1 = AirInterface.create("OOK", address=0xC8C8C, energenie_radio)

# Could also consider this a local network, with common parameters shared
# by all devices that use it.
#air2    = AirInterface.create("FSK", energenie_radio)

# scheduling would then become
# scheduler = Scheduler(energenie_radio)
# legacy1 = AirInterface.create("OOK", address=0xC8C8C, scheduler)
# air2    = AirInterface.create("FSK", scheduler
# so that when a device tries to transmit, it gets air interface specific
# settings added to it as appropriate, then the scheduler decides when
# to send and receive

# Somehow we need to associate devices with an air interface
# This might allow us to support multiple radios in the future too?
#legacy1.add(tv)

# cooperative loop could be energenie_radio.loop()
# or wrap a thread around it with start() but beware of thread context
# and thread safety.

import time

def test_without_registry():

    tv  = DeviceFactory.get_device("GreenButton", device_id=(0xC8C8C, 1))
    fan = DeviceFactory.get_device("AdaptorPlus", device_id=0x68b)

    while True:
        print("ON")
        tv.turn_on()
        fan.turn_off()
        time.sleep(2)

        print("OFF")
        tv.turn_off()
        fan.turn_on()
        time.sleep(1)


if __name__ == "__main__":
    test_without_registry()

# END
