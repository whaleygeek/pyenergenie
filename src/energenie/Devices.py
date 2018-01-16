# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices
# This table is mostly reverse-engineered from various websites and web catalogues.

##from lifecycle import *
try:
    # Python 2
    import OnAir
    import OpenThings
except ImportError:
    # Python 3
    from . import OnAir
    from . import OpenThings

# This level of indirection allows easy mocking for testing
ook_interface = OnAir.TwoBitAirInterface()
fsk_interface = OnAir.OpenThingsAirInterface()


MFRID_ENERGENIE                  = 0x04
MFRID                            = MFRID_ENERGENIE

##PRODUCTID_MIHO001               =        #         Home Hub
##PRODUCTID_MIHO002               =        #         OOK Control only
##PRODUCTID_MIHO003               = 0x0?   #         Hand Controller
PRODUCTID_MIHO004                = 0x01   #         Monitor only
PRODUCTID_MIHO005                = 0x02   #         Adaptor Plus
PRODUCTID_MIHO006                = 0x05   #         House Monitor
##PRODUCTID_MIHO007               = 0x0?   #         Double Wall Socket White
##PRODUCTID_MIHO008               = 0x0?   #         OOK: Single light switch white
##PRODUCTID_MIHO009 not used
##PRODUCTID_MIHO010 not used
##PRODUCTID_MIHO011 not used
##PRODUCTID_MIHO012 not used
PRODUCTID_MIHO013                = 0x03   #         eTRV
##PRODUCTID_MIHO014                       # OOK In-line Relay
##PRODUCTID_MIHO015 not used
##PRODUCTID_MIHO016 not used
##PRODUCTID_MIHO017
##PRODUCTID_MIHO018
##PRODUCTID_MIHO019
##PRODUCTID_MIHO020
##PRODUCTID_MIHO021               = 0x0?   #         Double Wall Socket Nickel
##PRODUCTID_MIHO022               = 0x0?   #         Double Wall Socket Chrome
##PRODUCTID_MIHO023               = 0x0?   #         Double Wall Socket Brushed Steel
##PRODUCTID_MIHO024               = 0x0?   #         OOK:Style Light Nickel
##PRODUCTID_MIHO025               = 0x0?   #         OOK:Style Light Chrome
##PRODUCTID_MIHO026               = 0x0?   #         OOK:Style Light Steel
##PRODUCTID_MIHO027 starter pack bundle
##PRODUCTID_MIHO028 eco starter pack
##PRODUCTID_MIHO029 heating bundle
##PRODUCTID_MIHO030 not used
##PRODUCTID_MIHO031 not used
PRODUCTID_MIHO032                 = 0x0C  # FSK motion sensor
PRODUCTID_MIHO033                 = 0x0D    # FSK open sensor
##PRODUCTID_MIHO034 not used
##PRODUCTID_MIHO035 not used
##PRODUCTID_MIHO036 not used
##PRODUCTID_MIHO037 Adaptor Plus Bundle
##PRODUCTID_MIHO038 2-gang socket Bundle
##PRODUCTID_MIHO039 2-gang socket Bundle black nickel
##PRODUCTID_MIHO040 2-gang socket Bundle chrome
##PRODUCTID_MIHO041 2-gang socket Bundle stainless steel
##PRODUCTID_MIHO069 Wall thermostat

# Default keys for OpenThings encryption and decryption
CRYPT_PID                        = 242
CRYPT_PIP                        = 0x0100

# OpenThings does not support a broadcast id,
# but Energenie added one for their MiHome Adaptors.
# This makes simple discovery possible.
BROADCAST_ID                     = 0xFFFFFF # Energenie broadcast


#----- DEFINED MESSAGE TEMPLATES ----------------------------------------------

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

JOIN_REQ = {
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


#----- CONTRACT WITH AIR-INTERFACE --------------------------------------------

# this might be a real air_interface (a radio), or an adaptor interface
# (a message scheduler with a queue).
#
#   synchronous send
#   synchronous receive
#TODO: asynchronous send (deferred)    - implies a callback on 'done, fail, timeout'
#TODO: asynchronous receive (deferred) - implies a callback on 'done, fail, timeout'

# air_interface has:
#   configure(parameters)
#   send(payload)
#   send(payload, parameters)
#   receive() -> (radio_measurements, address, payload)


#----- NEW DEVICE CLASSES -----------------------------------------------------

class Device():
    """A generic connected device abstraction"""
    def __init__(self, device_id=None, air_interface=None):
        self.air_interface = air_interface
        self.device_id = self.parse_device_id(device_id)
        class RadioConfig(): pass
        self.radio_config = RadioConfig()
        class Capabilities(): pass
        self.capabilities = Capabilities()
        self.updated_cb = None
        self.rxseq = 0

    def get_config(self):
        raise RuntimeError("There is no configuration for a base Device")

    @staticmethod
    def parse_device_id(device_id):
        """device_id could be a number, a hex string or a decimal string"""
        ##print("**** parsing: %s" % str(device_id))
        if device_id == None:
            raise ValueError("device_id is None, not allowed")

        if type(device_id) == int:
            return device_id # does not need to be parsed

        if type(device_id) == tuple or type(device_id) == list:
            # each part of the tuple could be encoded
            res = []
            for p in device_id:
                res.append(Device.parse_device_id(p))
            #TODO: could usefully convert to tuple here to be helpful
            return res

        if type(device_id) == str:
            # could be hex or decimal or strtuple or strlist
            if device_id == "":
                raise ValueError("device_id is blank, not allowed")
            elif device_id.startswith("0x"):
                return int(device_id, 16)
            elif device_id[0] == '(' and device_id[-1] == ')':
                ##print("**** parse tuple")
                inner = device_id[1:-1]
                parts = inner.split(',')
                ##print(parts)
                res = []
                for p in parts:
                    res.append(Device.parse_device_id(p))
                ##print(res)
                return res

            elif device_id[0] == '[' and device_id[-1] == ']':
                ##print("**** parse list")
                inner = device_id[1:-1]
                parts = inner.split(',')
                ##print(parts)
                res = []
                for p in parts:
                    res.append(Device.parse_device_id(p))
                #TODO: could usefully change to tuple here
                ##print(res)
                return res
            else:
                return int(device_id, 10)

        else:
            raise ValueError("device_id unsupported type or format, got: %s %s" % (type(device_id), str(device_id)))


    def has_switch(self):
        return hasattr(self.capabilities, "switch")

    def can_send(self):
        return hasattr(self.capabilities, "send")

    def can_receive(self):
        return hasattr(self.capabilities, "receive")

    def get_radio_config(self):
        return self.radio_config

    def get_last_receive_time(self): # ->timestamp
        """The timestamp of the last time any message was received by this device"""
        return self.last_receive_time

    def get_next_receive_time(self): # -> timestamp
        """An estimate of the next time we expect a message from this device"""
        pass

    def get_readings_summary(self):
        """Try to get a terse summary of all present readings"""

        try:
            r = self.readings
        except AttributeError:
            return "(no readings)"

        def shortname(name):
            parts = name.split('_')
            sn = ""
            for p in parts:
                sn += p[0].upper()
            return sn


        line = ""
        for rname in dir(self.readings):
            if not rname.startswith("__"):
                value = getattr(self.readings, rname)
                line += "%s:%s " % (shortname(rname), str(value))

        return line

        # for each reading
        #   call get_x to get the reading
        #   think of a very short name, perhaps first letter of reading name?
        #   add it to a terse string
        # return the string

    def get_receive_count(self):
        return self.rxseq

    def incoming_message(self, payload):
        """Entry point for a message to be processed"""
        #This is the base-class entry point, don't  override this, but override handle_message
        self.rxseq += 1
        self.handle_message(payload)
        if self.updated_cb != None:
            self.updated_cb(self, payload)

    def handle_message(self, payload):
        """Default handling for a new message"""
        print("incoming(unhandled): %s" % payload)

    def send_message(self, payload):
        print("send_message %s" % payload)
        # A raw device has no knowledge of how to send, the sub class provides that.

    def when_updated(self, callback):
        """Provide a callback handler to be called when a new message arrives"""
        self.updated_cb = callback
        # signature: update(self, message)

    def __repr__(self):
        return "Device()"


class EnergenieDevice(Device):
    """An abstraction for any kind of Energenie connected device"""
    def __init__(self, device_id=None, air_interface=None):
        Device.__init__(self, device_id, air_interface)

    def get_device_id(self): # -> id:int
        return self.device_id

    def __repr__(self):
        return "EnergenieDevice(%s)" % str(self.device_id)


class LegacyDevice(EnergenieDevice):
    DEFAULT_HOUSE_ADDRESS = 0x6C6C6

    """An abstraction for Energenie green button legacy OOK devices"""
    def __init__(self, device_id=None, air_interface=None):
        if air_interface == None:
            air_interface == ook_interface
        if device_id == None:
            device_id = (LegacyDevice.DEFAULT_HOUSE_ADDRESS, 1)
        elif type(device_id) == int:
            device_id = (LegacyDevice.DEFAULT_HOUSE_ADDRESS, device_id)
        elif type(device_id) == tuple and device_id[0] ==  None:
            device_id = (LegacyDevice.DEFAULT_HOUSE_ADDRESS, device_id[1])

        EnergenieDevice.__init__(self, device_id, ook_interface)
        #TODO: These are now just be implied by the ook_interface adaptor
        ##self.radio_config.frequency  = 433.92
        ##self.radio_config.modulation = "OOK"
        ##self.radio_config.codec      = "4bit"

    def __repr__(self):
        return "LegacyDevice(%s)" % str(self.device_id)

    def get_config(self):
        """Get the persistable config, enough to reconstruct this class from a factory"""
        return {
            "type":            self.__class__.__name__,
            "device_id":       self.device_id
        }


    def send_message(self, payload):
        if self.air_interface != None:
            self.air_interface.send(payload, radio_config=self.radio_config)
        else:
            d = self.device_id
            print("send_message(mock[%s]):%s" % (str(d), payload))


class MiHomeDevice(EnergenieDevice):
    """An abstraction for Energenie new style MiHome FSK devices"""
    def __init__(self, device_id=None, air_interface=None):
        if air_interface == None:
            air_interface = fsk_interface
        EnergenieDevice.__init__(self, device_id, air_interface)
        #TODO: These are now implied by the air_interface adaptor
        ##self.radio_config.frequency  = 433.92
        ##self.radio_config.modulation = "FSK"
        ##self.radio_config.codec      = "OpenThings"
        self.manufacturer_id         = MFRID_ENERGENIE
        self.product_id              = None

        #Different devices might have different PIP's
        #if we are cycling codes on each message?
        ##self.config.encryptPID = CRYPT_PID
        ##self.config.encryptPIP = CRYPT_PIP

    def get_config(self):
        """Get the persistable config, enough to reconstruct this class from a factory"""
        return {
            "type":            self.__class__.__name__,
            ##"manufacturer_id": self.manufacturer_id, # not needed, known by class
            ##"product_id":      self.product_id, # not needed, known by class
            "device_id":       self.device_id
        }

    def __repr__(self):
        return "MiHomeDevice(%s,%s,%s)" % (str(self.manufacturer_id), str(self.product_id), str(self.device_id))

    def get_manufacturer_id(self): # -> id:int
        return self.manufacturer_id

    def get_product_id(self): # -> id:int
        return self.product_id

    @staticmethod
    def get_join_req(mfrid, productid, deviceid):
        """Used for testing, synthesises a JOIN_REQ message from this device"""
        msg = OpenThings.Message(JOIN_REQ)
        msg["header_mfrid"]     = mfrid
        msg["header_productid"] = productid
        msg["header_sensorid"]  = deviceid
        return msg

    def join_ack(self):
        """Send a join-ack to the real device"""
        msg = OpenThings.Message(header_mfrid=MFRID_ENERGENIE, header_productid=self.product_id, header_sensorid=self.device_id)
        msg[OpenThings.PARAM_JOIN] = {"wr":False, "typeid":OpenThings.Value.UINT, "length":0}
        self.send_message(msg)

    ##def handle_message(self, payload):
    #override for any specific handling

    def send_message(self, payload):
        #TODO: interface with air_interface
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


#------------------------------------------------------------------------------

class OOKSwitch(LegacyDevice):
    """Any OOK controlled switch"""
    def __init__(self, device_id, air_interface=None):
        LegacyDevice.__init__(self, device_id, air_interface)
        self.radio_config.inner_times = 8
        self.capabilities.switch = True
        self.capabilities.receive = True

    def __repr__(self):
        return "OOKSwitch(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))


    def turn_on(self):
        #TODO: should this be here, or in LegacyDevice??
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

    def set_switch(self, state):
        if state:
            self.turn_on()
        else:
            self.turn_off()


class ENER002(OOKSwitch):
    """A green button switch"""
    def __repr__(self):
        return "ENER002(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))


class MIHO002(OOKSwitch):
    """A purple button MiHome switch"""
    def __repr__(self):
        return "MIHO002(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))


class MIHO014(OOKSwitch):
    """Energenie 3kW switchable relay"""
    def __repr__(self):
        return "MIHO014(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))


#------------------------------------------------------------------------------

class MiHomeLight(LegacyDevice):
    """Base for all MiHomeLight variants. Receive only OOK device"""
    def __init__(self, device_id, air_interface=None):
        LegacyDevice.__init__(self, device_id, air_interface)
        self.radio_config.inner_times = 75
        self.capabilities.switch = True
        self.capabilities.receive = True

    def __repr__(self):
        return "MiHomeLight(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))

    def turn_on(self):
        #TODO: should this be here, or in LegacyDevice??
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

    def set_switch(self, state):
        if state:
            self.turn_on()
        else:
            self.turn_off()


class MIHO008(MiHomeLight):
    """White finish"""
    def __repr__(self):
        return "MIHO008(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))

class MIHO024(MiHomeLight):
    """Black Nickel Finish"""
    def __repr__(self):
        return "MIHO024(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))

class MIHO025(MiHomeLight):
    """Chrome Finish"""
    def __repr__(self):
        return "MIHO025(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))

class MIHO026(MiHomeLight):
    """Brushed Steel Finish"""
    def __repr__(self):
        return "MIHO026(%s,%s)" % (str(hex(self.device_id[0])), str(hex(self.device_id[1])))


#------------------------------------------------------------------------------

class MIHO004(MiHomeDevice):
    """Energenie Monitor-only Adaptor"""
    def __init__(self, device_id, air_interface=None):
        MiHomeDevice.__init__(self, device_id, air_interface)
        self.product_id = PRODUCTID_MIHO004
        class Readings():
            voltage        = None
            frequency      = None
            current        = None
            apparent_power = None
            reactive_power = None
            real_power     = None
        self.readings = Readings()
        self.radio_config.inner_times = 4
        self.capabilities.send = True
        self.capabilities.switch = True

    def __repr__(self):
        return "MIHO004(%s)" % str(hex(self.device_id))

    @staticmethod
    def get_join_req(deviceid):
        """Get a synthetic join request from this device, for testing"""
        return MiHomeDevice.get_join_req(MFRID_ENERGENIE, PRODUCTID_MIHO004, deviceid)

    def handle_message(self, payload):
        ##print("MIHO005 new data %s %s" % (self.device_id, payload))
        for rec in payload["recs"]:
            paramid = rec["paramid"]
            #TODO: consider making this table driven and allowing our base class to fill our readings in for us
            #  then just define the mapping table in __init__ (i.e. paramid->Readings field name)
            value = rec["value"]
            if paramid == OpenThings.PARAM_VOLTAGE:
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


#------------------------------------------------------------------------------

class MIHO005(MiHomeDevice):
    """An Energenie MiHome Adaptor Plus"""
    def __init__(self, device_id, air_interface=None):
        MiHomeDevice.__init__(self, device_id, air_interface)
        self.product_id = PRODUCTID_MIHO005
        class Readings():
            switch         = None
            voltage        = None
            frequency      = None
            current        = None
            apparent_power = None
            reactive_power = None
            real_power     = None
        self.readings = Readings()
        self.radio_config.inner_times = 4
        self.capabilities.send = True
        self.capabilities.receive = True
        self.capabilities.switch = True

    def __repr__(self):
        return "MIHO005(%s)" % str(hex(self.device_id))

    @staticmethod
    def get_join_req(deviceid):
        """Get a synthetic join request from this device, for testing"""
        return MiHomeDevice.get_join_req(MFRID_ENERGENIE, PRODUCTID_MIHO004, deviceid)

    def handle_message(self, payload):
        ##print("MIHO005 new data %s %s" % (self.device_id, payload))
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
        #TODO: header construction should be in MiHomeDevice as it is shared?
        payload = OpenThings.Message(SWITCH)
        payload.set(header_productid=self.product_id,
                    header_sensorid=self.device_id,
                    recs_SWITCH_STATE_value=True)
        self.send_message(payload)

    def turn_off(self):
        #TODO: header construction should be in MiHomeDevice as it is shared?
        payload = OpenThings.Message(SWITCH)
        payload.set(header_productid=self.product_id,
                    header_sensorid=self.device_id,
                    recs_SWITCH_STATE_value=False)
        self.send_message(payload)

    def set_switch(self, state):
        if state:
            self.turn_on()
        else:
            self.turn_off()

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


#------------------------------------------------------------------------------

class MIHO006(MiHomeDevice):
    """An Energenie MiHome Home Monitor"""
    def __init__(self, device_id, air_interface=None):
        MiHomeDevice.__init__(self, device_id, air_interface)
        self.product_id = PRODUCTID_MIHO006
        class Readings():
            battery_voltage = None
            current         = None
            apparent_power  = None
        self.readings = Readings()
        self.capabilities.send = True

    def __repr__(self):
        return "MIHO006(%s)" % str(hex(self.device_id))

    def handle_message(self, payload):
        for rec in payload["recs"]:
            paramid = rec["paramid"]
            #TODO: consider making this table driven and allowing our base class to fill our readings in for us
            #TODO: consider using @OpenThings.parameter as a decorator to the receive function
            #it will then register a handler for that message for itself as a handler
            #we still need Readings() defined too as a cache. The decorator could add
            #an entry into the cache too for us perhaps?
            if "value" in rec:
                value = rec["value"]
                if paramid == OpenThings.PARAM_VOLTAGE:
                    self.readings.battery_voltage = value
                elif paramid == OpenThings.PARAM_CURRENT:
                    self.readings.current = value
                elif paramid == OpenThings.PARAM_APPARENT_POWER:
                    self.readings.apparent_power = value
                else:
                    try:
                        param_name = OpenThings.param_info[paramid]['n'] # name
                    except:
                        param_name = "UNKNOWN_%s" % str(hex(paramid))
                    print("unwanted paramid: %s" % param_name)
        pass

    def get_battery_voltage(self): # -> voltage:float
        return self.readings.battery_voltage

    def get_current(self): # -> current:float
        return self.readings.current

    def get_apparent_power(self): # -> power:float
        return self.reading.apparent_power



#------------------------------------------------------------------------------

class MIHO013(MiHomeDevice):
    """An Energenie MiHome eTRV Radiator Valve"""
    def __init__(self, device_id, air_interface=None):
        MiHomeDevice.__init__(self, device_id, air_interface)
        self.product_id = PRODUCTID_MIHO013
        class Readings():
            battery_voltage      = None
            ambient_temperature  = None
            pipe_temperature     = None
            setpoint_temperature = None
            valve_position       = None
        self.readings = Readings()
        self.radio_config.inner_times = 10
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
        self.send_message("set setpoint temp") #TODO: command

    def get_valve_position(self): # -> position:int?
        pass #TODO: is this possible?

    def set_valve_position(self, position):
        pass #TODO: command, is this possible?
        self.send_message("set valve pos") #TODO

    #TODO: difference between 'is on and 'is requested on'
    #TODO: difference between 'is off' and 'is requested off'
    #TODO: switch state might be 'unknown' if not heard.
    #TODO: switch state might be 'turning_on' or 'turning_off' if send request and not heard response yet

    def turn_on(self): # command
        pass #TODO: command i.e. valve position?
        self.send_message("turn on") #TODO

    def turn_off(self): # command
        pass #TODO: command i.e. valve position?
        self.send_message("turn off") #TODO

    def is_on(self): # query last known reported state (unknown if changing?)
        pass #TODO: i.e valve is not completely closed?

    def is_off(self): # query last known reported state (unknown if changing?)
        pass #TODO: i.e. valve is completely closed?


#------------------------------------------------------------------------------

class MIHO032(MiHomeDevice):
    """An Energenie Motion Sensor"""
    def __init__(self, device_id, air_interface=None):
        MiHomeDevice.__init__(self, device_id, air_interface)
        self.product_id = PRODUCTID_MIHO032
        class Readings():
            switch_state = None
            battery_alarm = None
        self.readings = Readings()
        self.capabilities.send = True

    def __repr__(self):
        return "MIHO032(%s)" % str(hex(self.device_id))

    def handle_message(self, payload):
        ##print("MIHO032 new data %s %s" % (self.device_id, payload))
        for rec in payload["recs"]:
            paramid = rec["paramid"]
            #TODO: consider making this table driven and allowing our base class to fill our readings in for us
            #TODO: consider using @OpenThings.parameter as a decorator to the receive function
            #it will then register a handler for that message for itself as a handler
            #we still need Readings() defined too as a cache. The decorator could add
            #an entry into the cache too for us perhaps?
            if "value" in rec:
                value = rec["value"]
                if paramid == OpenThings.PARAM_MOTION_DETECTOR:
                    self.readings.switch_state = ((value == True) or (value != 0))
                elif paramid == OpenThings.PARAM_ALARM:
                    if value == 0x42: # battery alarming
                        self.readings.battery_alarm = True
                    elif value == 0x62: # battery not alarming
                        self.readings.battery_alarm = False
                else:
                    try:
                        param_name = OpenThings.param_info[paramid]['n'] # name
                    except:
                        param_name = "UNKNOWN_%s" % str(hex(paramid))
                    print("unwanted paramid: %s" % param_name)

    def get_switch_state(self): # -> switch:bool
        return self.readings.switch_state

    def get_battery_alarm(self): # -> alarm:bool
        return self.readings.battery_alarm

#------------------------------------------------------------------------------

class MIHO033(MiHomeDevice):
    """An Energenie Open Sensor"""
    def __init__(self, device_id, air_interface=None):
        MiHomeDevice.__init__(self, device_id, air_interface)
        self.product_id = PRODUCTID_MIHO033
        class Readings():
            switch_state = None
        self.readings = Readings()
        self.capabilities.send = True

    def __repr__(self):
        return "MIHO033(%s)" % str(hex(self.device_id))

    def handle_message(self, payload):
        ##print("MIHO033 new data %s %s" % (self.device_id, payload))
        for rec in payload["recs"]:
            paramid = rec["paramid"]
            #TODO: consider making this table driven and allowing our base class to fill our readings in for us
            #TODO: consider using @OpenThings.parameter as a decorator to the receive function
            #it will then register a handler for that message for itself as a handler
            #we still need Readings() defined too as a cache. The decorator could add
            #an entry into the cache too for us perhaps?
            if "value" in rec:
                value = rec["value"]
                if paramid == OpenThings.PARAM_DOOR_SENSOR:
                    self.readings.switch_state = ((value == True) or (value != 0))
                else:
                    try:
                        param_name = OpenThings.param_info[paramid]['n'] # name
                    except:
                        param_name = "UNKNOWN_%s" % str(hex(paramid))
                    print("unwanted paramid: %s" % param_name)

    def get_switch_state(self): # -> switch:bool
        return self.readings.switch_state


#----- DEVICE FACTORY ---------------------------------------------------------

# This is a singleton, but might not be in the future.
# i.e. we might have device factories for lots of different devices.
# and a DeviceFactory could auto configure it's set of devices
# with a specific air_interface for us.
# i.e. this might be the EnergenieDeviceFactory, there might be others
# for other product ranges like wirefree doorbells


class DeviceFactory():
    """A place to come to, to get instances of device classes"""
    # If you know the name of the device, use this table
    device_from_name = {
        # official name            friendly name
        "ENER002":     ENER002,    "GreenButton":       ENER002, # OOK(rx)
        "MIHO002":     MIHO002,    "Controller":        MIHO002, # OOK(rx)
        "MIHO004":     MIHO004,    "Monitor":           MIHO004, # FSK(rx)
        "MIHO005":     MIHO005,    "AdaptorPlus":       MIHO005, # FSK(tx,rx)
        "MIHO006":     MIHO006,    "HomeMonitor":       MIHO006, # FSK(tx)
        "MIHO008":     MIHO008,    "MiHomeLightWhite":  MIHO008, # OOK(rx)
        "MIHO013":     MIHO013,    "eTRV":              MIHO013, # FSK(tx,rx)
        "MIHO014":     MIHO014,    "3kWRelay":          MIHO014, # OOK(rx)
        "MIHO024":     MIHO024,    "MiHomeLightBlack":  MIHO024, # OOK(rx)
        "MIHO025":     MIHO025,    "MiHomeLightChrome": MIHO025, # OOK(rx)
        "MIHO026":     MIHO026,    "MiHomeLightSteel":  MIHO026, # OOK(rx)
        "MIHO032":     MIHO032,    "MotionSensor":      MIHO032, # FSK(tx)
        "MIHO033":     MIHO033,    "OpenSensor":        MIHO033, # FSK(tx)
    }

    #TODO: These are MiHome devices only, but might add in mfrid prefix too
    # If you know the mfrid, productid of the device, use this table
    device_from_id = {
        #ENER002 is anOOK
        #MIHO002 control only switch is an OOK
        PRODUCTID_MIHO004: MIHO004,
        PRODUCTID_MIHO005: MIHO005,
        PRODUCTID_MIHO006: MIHO006,
        #MIHO008 is an OOK
        PRODUCTID_MIHO013: MIHO013,
        #MIHO014 is an OOK
        #MIHO024 is an OOK
        #MIHO025 is an OOK
        #MIHO026 is an OOK
        PRODUCTID_MIHO032: MIHO032,
        PRODUCTID_MIHO033: MIHO033
    }

    default_air_interface = None

    @staticmethod
    def set_default_air_interface(air_interface):
        DeviceFactory.default_air_interface = air_interface

    @staticmethod
    def keys():
        return DeviceFactory.device_from_name.keys()

    @staticmethod
    def get_device_from_name(name, device_id=None, air_interface=None, **kwargs):
        """Get a device by name, construct a new instance"""
        # e.g. This is useful when creating device class instances from a human readable config
        if not name in DeviceFactory.device_from_name:
            raise ValueError("Unsupported device:%s" % name)

        c = DeviceFactory.device_from_name[name]
        if air_interface == None:
            air_interface = DeviceFactory.default_air_interface
        return c(device_id, air_interface, **kwargs)

    @staticmethod
    def get_device_from_id(id, device_id=None, air_interface=None):
        """Get a device by it's id, construct a new instance"""
        # e.g. This is useful when recreating device class instances from a persisted registry
        if not id in DeviceFactory.device_from_id:
            raise ValueError("Unsupported device id:%s" % id)

        c = DeviceFactory.device_from_id[id]
        if air_interface == None:
            air_interface = DeviceFactory.default_air_interface
        i = c(device_id, air_interface)
        print(i)
        return i


# END

