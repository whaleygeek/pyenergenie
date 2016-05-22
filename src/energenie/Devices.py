# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices
# This table is mostly reverse-engineered from various websites and web catalogues.

from lifecycle import *
import OnAir
import OpenThings

# This level of indirection allows easy mocking for testing
ook_interface = OnAir.TwoBitAirInterface()
fsk_interface = OnAir.OpenThingsAirInterface()


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
#Still used in deprecated methods in Registry.py

@deprecated
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
#still used in switch.py demo (will be until device classes deployed into tests)

@deprecated
def hasSwitch(mfrid, productid):
    if mfrid != MFRID:                  return False
    if productid == PRODUCTID_MIHO005:  return True
    return False


#----- DEFINED MESSAGE TEMPLATES ----------------------------------------------

##TODO: This should really be in OpenThings.Message

import copy

def create_message(message):
    return copy.deepcopy(message)

SWITCH = {
    "header": {
        "mfrid":       MFRID_ENERGENIE,
        "productid":   PRODUCTID_MIHO005,
        "encryptPIP":  CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      True,
            "paramid": OpenThings.PARAM_SWITCH_STATE,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        }
    ]
}


JOIN_ACK = {
    "header": {
        "mfrid":       0, # FILL IN
        "productid":   0, # FILL IN
        "encryptPIP":  CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_JOIN,
            "typeid":  OpenThings.Value.UINT,
            "length":  0
        }
    ]
}


REGISTERED_SENSOR = {
    "header": {
        "mfrid":       MFRID_ENERGENIE,
        "productid":   0, # FILL IN
        "encryptPIP":  CRYPT_PIP,
        "sensorid":    0 # FILL IN
    }
}


MIHO005_REPORT = {
    "header": {
        "mfrid":       MFRID_ENERGENIE,
        "productid":   PRODUCTID_MIHO005,
        "encryptPIP":  CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_SWITCH_STATE,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_VOLTAGE,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_CURRENT,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_FREQUENCY,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_REAL_POWER,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_REACTIVE_POWER,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },
        {
            "wr":      False,
            "paramid": OpenThings.PARAM_APPARENT_POWER,
            "typeid":  OpenThings.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        },

    ]
}

def send_join_ack(radio, mfrid, productid, sensorid):
    # send back a JOIN ACK, so that join light stops flashing
    response = OpenThings.alterMessage(create_message(JOIN_ACK),
        header_mfrid=mfrid,
        header_productid=productid,
        header_sensorid=sensorid)
    p = OpenThings.encode(response)
    radio.transmitter()
    radio.transmit(p, inner_times=2)
    radio.receiver()



#----- CONTRACT WITH AIR-INTERFACE --------------------------------------------

# this might be a real air_interface (a radio), or an adaptor interface
# (a message scheduler with a queue).
#
#   synchronous send
#   synchronous receive
#   TODO: asynchronous send (deferred)    - implies a callback on 'done, fail, timeout'
#   TODO: asynchronous receive (deferred) - implies a callback on 'done, fail, timeout'

# air_interface has:
#   configure(parameters)
#   send(payload)
#   send(payload, parameters)
#   receive() -> (radio_measurements, address, payload)


#----- NEW DEVICE CLASSES -----------------------------------------------------

class Device():
    """A generic connected device abstraction"""
    def __init__(self, air_interface):
        self.air_interface = air_interface
        class Config(): pass
        self.config = Config()
        class Capabilities(): pass
        self.capabilities = Capabilities()

    def has_switch(self):
        return hasattr(self.capabilities, "switch")

    def can_send(self):
        return hasattr(self.capabilities, "send")

    def can_receive(self):
        return hasattr(self.capabilities, "receive")

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
        print("incoming(unhandled):%s" % payload)

    def send_message(self, payload):
        print("send_message %s" % payload)
        # A raw device has no knowledge of how to send, the sub class provides that.

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
    def __init__(self):
        EnergenieDevice.__init__(self, ook_interface)
        self.config.frequency  = 433.92
        self.config.modulation = "OOK"
        self.config.codec      = "4bit"

    def __repr__(self):
        return "LegacyDevice(%s)" % str(self.device_id)

    def send_message(self, payload):
        ####HERE#### interface with air_interface
        # Encode the payload two bits per byte as per OOK spec
        #TODO, should we just pass a payload (as a pydict or tuple) to the air_interface adaptor
        #and let it encode it, to be consistent with the FSK MiHome devices?
        #payload could be a 3-tuple of (house_address, device_address, state)
        #bytes = TwoBit.build_switch_msg(payload, house_address=self.device_id[0], device_address=self.device_id[1])

        if self.air_interface != None:
            #TODO: might want to send the config, either as a send parameter,
            #or by calling air_interface.configure() first?
            #i.e. radio.modulation(MODULATION_OOK)
            self.air_interface.send(payload) #TODO: or (ha, da, s)
        else:
            d = self.device_id
            print("send_message(mock[%s]):%s" % (str(d), payload))


class MiHomeDevice(EnergenieDevice):
    """An abstraction for Energenie new style MiHome FSK devices"""
    def __init__(self, device_id=None):
        EnergenieDevice.__init__(self, fsk_interface, device_id)
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

    def join_ack(self):
        """Send a join-ack to the real device"""
        self.send_message("join ack") # TODO

    def incoming_message(self, payload):
        ####HERE#### interface with air_interface
        """Handle incoming messages for this device"""
        #NOTE: we must have already decoded the message with OpenThings to be able to get the addresses out
        # so payload at this point must be a pydict?

        #we know at this point that it's a FSK message
        #OpenThingsAirInterface has already decrypted and decoded
        #so we get a pydict payload here with header and recs in it
        #the header has the address which is used for routing

        #TODO join request might be handled generically here
        #TODO: subclass can override and call back to this if it wants to
        raise RuntimeError("Method unimplemented") #TODO

    def send_message(self, payload):
        ####HERE#### interface with air_interface
        #is payload a pydict with header at this point, and we have to call OpenThings.encode?
        #should the encode be done here, or in the air_interface adaptor?

        #TODO: at what point is the payload turned into a pydict?
        #TODO: We know it's going over OpenThings,
        #do we call OpenThings.encode(payload) here?
        #also OpenThings.encrypt() - done by encode() as default
        if self.air_interface != None:
            #TODO: might want to send the config, either as a send parameter,
            #or by calling air_interface.configure() first?
            self.air_interface.send(payload)
        else:
            m = self.manufacturer_id
            p = self.product_id
            d = self.device_id
            print("send_message(mock[%s %s %s]):%s" % (str(m), str(p), str(d), payload))


class ENER002(LegacyDevice):
    """A green-button switch"""
    def __init__(self, device_id=None):
        LegacyDevice.__init__(self)
        self.device_id = device_id # (house_address, device_index)
        self.config.tx_repeats = 8
        self.capabilities.switch = True
        self.capabilities.receive = True

    def turn_on(self):
        #TODO should this be here, or in LegacyDevice??
        #addressing should probably be in LegacyDevice
        #child devices might interpret the command differently
        payload = {
            "house_address":  self.device_id[0],
            "device_index":   self.device_id[1],
            "on":             True
        }
        self.send_message(payload)

    def turn_off(self):
        #TODO: should this be here, or in LegacyDevice???
        #addressing should probably be in LegacyDevice
        #child devices might interpret the command differently
        payload = {
            "house_address":  self.device_id[0],
            "device_index":   self.device_id[1],
            "on":             False
        }
        self.send_message(payload)


class MIHO005(MiHomeDevice):
    """An Energenie MiHome Adaptor Plus"""
    def __init__(self, device_id=None):
        MiHomeDevice.__init__(self)
        self.product_id = PRODUCTID_MIHO005
        self.device_id  = device_id
        class Readings():
            switch         = None
            voltage        = None
            frequency      = None
            current        = None
            apparent_power = None
            reactive_power = None
            real_power     = None
        self.readings = Readings()
        self.config.tx_repeats = 4
        self.capabilities.send = True
        self.capabilities.receive = True
        self.capabilities.switch = True

    def incoming_message(self, payload):
        ####HERE####
        for rec in payload["recs"]:
            paramid = rec["paramid"]
            #TODO: consider making this table driven and allowing our base class to fill our readings in for us
            #  then just define the mapping table in __init__ (i.e. paramid->Readings field name)
            value = rec["value"]
            if paramid == OpenThings.PARAM_SWITCH_STATE:
                self.readings.switch = ((value == True) or (value != 0))
            elif paramid == OpenThings.PARAM_VOLTAGE:
                self.readings.voltage = value
            elif paramid == OpenThings.PARAM_CURRENT:
                self.readings.current = value
            elif paramid == OpenThings.PARAM_REAL_POWER:
                self.readings.real_power = value
            elif paramid == OpenThings.PARAM_APPARENT_POWER:
                self.readings.apparent_power = value
            elif paramid == OpenThings.PARAM_REACTIVE_POWER:
                self.readings.reactive_power = value
            elif paramid == OpenThings.PARAM_FREQUENCY:
                self.readings.frequency = value
            else:
                try:
                    param_name = OpenThings.param_info[paramid]['n'] # name
                except:
                    param_name = "UNKNOWN_%s" % str(hex(paramid))
                print("unwanted paramid: %s" % param_name)

    def get_readings(self): # -> readings:pydict
        """A way to get all readings as a single consistent set"""
        return self.readings

    def turn_on(self):
        #TODO: header construction should be in MiHomeDevice as it is shared
        payload = OpenThings.alterMessage(
            create_message(SWITCH),
            header_productid = self.product_id,
            header_sensorid  = self.device_id,
            recs_0_value     = True)
        self.send_message(payload)

    def turn_off(self):
        #TODO: header construction should be in MiHomeDevice as it is shared
        payload = OpenThings.alterMessage(
            create_message(SWITCH),
            header_productid = self.product_id,
            header_sensorid  = self.device_id,
            recs_0_value     = False)
        self.send_message(payload)

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
        if self.readings.voltage == None:
            raise RuntimeError("No voltage reading received yet")
        return self.readings.voltage

    def get_frequency(self): # -> frequency:float
        """Last stored state of frequency reading, None if unknown"""
        if self.readings.frequency == None:
            raise RuntimeError("No frequency reading received yet")
        return self.readings.frequency

    def get_apparent_power(self): # ->power:float
        """Last stored state of apparent power reading, None if unknown"""
        if self.readings.apparent_power == None:
            raise RuntimeError("No apparent power reading received yet")
        return self.readings.apparent_power

    def get_reactive_power(self): # -> power:float
        """Last stored state of reactive power reading, None if unknown"""
        if self.readings.reactive_power == None:
            raise RuntimeError("No reactive power reading received yet")
        return self.readings.reactive_power

    def get_real_power(self): #-> power:float
        """Last stored state of real power reading, None if unknown"""
        if self.readings.real_power == None:
            raise RuntimeError("No real power reading received yet")
        return self.readings.real_power


class MIHO006(MiHomeDevice):
    """An Energenie MiHome Home Monitor"""
    def __init__(self, device_id=None):
        MiHomeDevice.__init__(self)
        self.product_id = PRODUCTID_MIHO006
        self.device_id  = device_id
        class Readings():
            battery_voltage = None
            current         = None
        self.readings = Readings()
        self.capabilities.send = True

    def get_battery_voltage(self): # -> voltage:float
        return self.readings.battery_voltage

    def get_current(self): # -> current:float
        return self.readings.current


class MIHO013(MiHomeDevice):
    """An Energenie MiHome eTRV Radiator Valve"""
    def __init__(self, device_id=None):
        MiHomeDevice.__init__(self)
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
        self.capabilities.send = True
        self.capabilities.receive = True

    def get_battery_voltage(self): # ->voltage:float
        return self.readings.battery_voltage

    def get_ambient_temperature(self): # -> temperature:float
        return self.readings.ambient_temperature

    def get_pipe_temperature(self): # -> temperature:float
        return self.readings.pipe_temperature

    def get_setpoint_temperature(self): #-> temperature:float
        return self.readings.setpoint_temperature

    def set_setpoint_temperature(self, temperature):
        self.send_message("set setpoint temp") # TODO command

    def get_valve_position(self): # -> position:int?
        pass # TODO is this possible?

    def set_valve_position(self, position):
        pass # TODO command, is this possible?
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

# END

