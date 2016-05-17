# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices
# This table is mostly reverse-engineered from various websites and web catalogues.

MFRID                            = 0x04

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
    if mfrid == MFRID:
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
    def __init__(self, air_interface):
        self.air_interface = air_interface

    def get_manufacturer_id(self): # -> id:int
        pass

    def get_product_id(self): # -> id:int
        pass

    def get_sensor_id(self): # -> id:int
        pass

    def get_last_receive_time(self): # ->timestamp
        pass

    def get_last_send_time(self): # -> timestamp
        pass

    def get_next_receive_time(self): # -> timestamp
        pass

    def get_next_send_time(self): # -> timestamp
        pass

    def incoming_message(self, payload):
        pass
        # incoming_message (OOK or OpenThings as appropriate, stripped of header? decrypted, decoded to pydict)

    def send_message(self, payload):
        pass
        # send_message (a link out to the transport, could be mocked, for example)


class EnergenieDevice(Device):
    def __init__(self, air_interface):
        Device.__init__(self, air_interface)

    def get_radio_config(self): # -> default config
        # get_radio_config -> config_selector? (freq, modulation) config_parameters? (inner_repeats, delay, outer_repeats)
        pass

    def has_switch(self): # -> default False
        pass

    def can_send(self): # -> default False
        pass

    def can_receive(self): # -> default False
        pass


class LegacyDevice(EnergenieDevice):
    def __init__(self, air_interface):
        EnergenieDevice.__init__(self, air_interface)

    def get_radio_config(self): # -> config
        pass
        # freq = 433.92MHz
        # modulation = OOK
        # codec = 4bit


class MiHomeDevice(EnergenieDevice):
    def __init__(self, air_interface):
        EnergenieDevice.__init__(self, air_interface)

    def get_radio_config(self): # -> config
        pass
        # freq = 433.92MHz
        # modulation = FSK
        # codec = OpenThings


class ENER002(LegacyDevice):
    def __init__(self, air_interface):
        LegacyDevice.__init__(self, air_interface)

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def can_send(self): # -> True
        pass


class MIHO005(MiHomeDevice): # Adaptor Plus
    def __init__(self, air_interface):
        MiHomeDevice.__init__(self, air_interface)

    def get_radio_config(self):
        pass
        # + tx_repeats = 4

    def can_send(self): # -> True
        pass

    def can_receive(self): # -> True
        pass

    def get_readings(self): # -> readings:pydict
        pass
        # a way to get all readings as a single consistent set

    def turn_on(self):
        pass # command request

    def turn_off(self):
        pass # command request

    #TODO: difference between 'is on and 'is requested on'
    #TODO: difference between 'is off' and 'is requested off'
    #TODO: switch state might be 'unknown' if not heard.
    #TODO: switch state might be 'turning_on' or 'turning_off' if send request and not heard response yet

    def is_on(self): # -> boolean
        pass
        # cached view of last received switch state

    def is_off(self): # -> boolean
        pass
        # cached view of last received switch state

    def get_switch(self): # -> boolean
        pass
        # cached view of last received switch state

    def get_voltage(self): # -> voltage:float
        pass
        # cached view of last received voltage

    def get_frequency(self): # -> frequency:float
        pass
        # cached view of last received frequency

    def get_apparent_power(self): # ->power:float
        pass
        # cached view of last apparent power reading

    def get_reactive_power(self): # -> power:float
        pass
        # cached view of last reactive power reading

    def get_real_power(self): #-> power:float
        pass
        # cached view of last real power reading


class MIHO006(MiHomeDevice): # Home Monitor
    def __init__(self, air_interface):
        MiHomeDevice.__init__(self, air_interface)

    def get_readings(self): # -> readings:pydict
        pass
        # a consistent set of all readings together

    def can_send(self): # -> True
        pass

    def get_battery_voltage(self): # -> voltage:float
        pass
        # cached view of last battery voltage reading

    def get_current(self): # -> current:float
        pass
        # cached view of last current reading


class MIHO012(MiHomeDevice): # eTRV
    def __init__(self, air_interface):
        MiHomeDevice.__init__(self, air_interface)

    def get_radio_config(self): # -> parameters
        pass
        # + tx_repeats = 10

    def can_send(self): # -> True
        pass

    def can_receive(self): # -> True
        pass

    def get_readings(self): # -> readings:pydict
        pass
        # cached view of all readings together

    def get_battery_voltage(self): # ->voltage:float
        pass
        # cached view of last voltage reading

    def get_ambient_temperature(self): # -> temperature:float
        pass
        # cached view of last temp reading

    def get_pipe_temperature(self): # -> temperature:float
        pass
        # cached view of last temp reading

    def get_setpoint_temperature(self): #-> temperature:float
        pass
        # cached view of last temp reading

    def set_setpoint_temperature(self, temperature):
        pass

    def get_valve_position(self): # -> position:int?
        pass

    def set_valve_position(self, position):
        pass

    #TODO: difference between 'is on and 'is requested on'
    #TODO: difference between 'is off' and 'is requested off'
    #TODO: switch state might be 'unknown' if not heard.
    #TODO: switch state might be 'turning_on' or 'turning_off' if send request and not heard response yet

    def turn_on(self): # command
        pass

    def turn_off(self): # command
        pass

    def is_on(self): # query last known reported state (unknown if changing?)
        pass

    def is_off(self): # query last known reported state (unknown if changing?)
        pass


#----- DEVICE FACTORY ---------------------------------------------------------

class DeviceFactory():
    """A place to come to, to get instances of device classes"""
    devices = {
        # official name            friendly name
        "ENER002":     ENER002,    "GreenButton": ENER002,
        "MIHO005":     MIHO005,    "AdaptorPlus": MIHO005,
        "MIHO006":     MIHO006,    "HomeMonitor": MIHO006,
        "MIHO012":     MIHO012,    "eTRV":        MIHO012,
    }

    @staticmethod
    def get_device(name):
        """Get a device by name, construct a new instance"""
        c = DeviceFactory.devices[name]
        return c()


#----- TEMPORARY TEST HARNESS -------------------------------------------------

import time

# Getting devices, without a registry yet
def test():
    #hmm: need two addresses for legacy
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

    # auto knitting?
    # DeviceFactory.set_air_interface(energenie_radio)
    # future get_device causes the air interface to be knitted up to the device
    # along with receive callbacks for asynchronous receive and update.

    # cooperative loop could be energenie_radio.loop()
    # or wrap a thread around it with start() but beware of thread context
    # and thread safety.


    tv  = DeviceFactory.get_device("GreenButton", address=(0xC8C8C, 1))
    fan = DeviceFactory.get_device("AdaptorPlus", address=0x68b)

    # With the registry, these would be added, so that they could be auto restored
    # on next boot
    # Registry.add(tv)
    # Registry.add(fan)

    # Note, when adding registry, all of this data will be stored in the persisted
    # registry, just start the registry and it creates all your object variables
    # for you from it's metadata.
    # Registry.start(some_context)
    # where some_context is the scope that the variables tv and fan are created in.

    while True:
        tv.turn_on()
        fan.turn_off()
        time.sleep(2)

        tv.turn_off()
        fan.turn_on()
        time.sleep(1)

if __name__ == "__main__":
    test()

# END
