# OnAir.py  19/05/2016  D.J.Whale
#
# A set of adaptors to allow device classes to interact with radio interfaces.
# At the moment, the main purpose of this abstraction is to prevent the need
# for device classes to know specifics about radio technology and focus
# on the device aspects only.
#
# In the future, this will be a useful point in the architecture to add
# an intelligent message scheduler, that learns the report patterns of
# specific devices, builds a timeslotted schedule, and schedules transmits
# into mostly free slots.
#
# NOTE: This also might include intelligent power level selection based
# on RSSI reports from different devices.

import time

try:
    # Python 2
    import OpenThings
    import TwoBit
    import radio
    from lifecycle import *

except ImportError:
    # Python 3
    from . import OpenThings
    from . import TwoBit
    from . import radio
    from .lifecycle import *

class OpenThingsAirInterface():
    def __init__(self):
        self.radio = radio # aids mocking later

        class RadioDefaults():
            frequency     = 433.92
            modulation    = radio.RADIO_MODULATION_FSK

        class TxDefaults(RadioDefaults):
            ##power_level   = 0
            inner_times   = 4
            outer_delay   = 0
            outer_times   = 1
        self.tx_defaults = TxDefaults()

        class RxDefaults(RadioDefaults):
            poll_rate     = 100  #ms
            timeout       = 1000 #ms
        self.rx_defaults = RxDefaults()

    ##@log_method
    def send(self, payload, radio_config=None):
        #   payload is a pydict suitable for OpenThings
        #   radio_params is an overlay on top of radio tx defaults
        p = OpenThings.encode(payload)

        # Set radio defaults, if no override
        outer_times = self.tx_defaults.outer_times
        outer_delay = self.tx_defaults.outer_delay
        inner_times = self.tx_defaults.inner_times

        # Merge any wanted radio params, if provided
        if radio_config != None:
            try:
                outer_times = radio_config.outer_times
            except AttributeError: pass
            try:
                outer_delay = radio_config.outer_delay
            except AttributeError: pass
            try:
                inner_times = radio_config.inner_times
            except AttributeError: pass

        radio.transmitter(fsk=True)
        ##print("inner times %s" % inner_times)
        radio.transmit(p, outer_times=outer_times, inner_times=inner_times, outer_delay=outer_delay)
        # radio auto-returns to previous state after transmit completes

    ##@log_method
    def receive(self, radio_config=None): # -> (radio_measurements, address or None, payload or None)
        #   radio_params is an overlay on top of radio rx defaults (e.g. poll rate, timeout, min payload, max payload)
        #   radio_measurements might include rssi reading, short payload report, etc
        pass # TODO
        #TODO: set radio to receive mode
        #TODO: merge radio_params with self.tx_defaults
        #TODO: configure radio modulation based on merged params

        #TODO: poll radio at rate until timeout or received
        #TODO: start timeout timer
        payload = None
        radio.receiver(fsk=True)
        while True: # timer not expired
            if radio.is_receive_waiting():
                payload = radio.receive() #TODO: payload, radio_measurements = radio.receive()
                now = time.time()
                p = OpenThings.decode(payload, receive_timestamp=now)
                #TODO: if crc failure, report it, but keep trying
                #if crc check passes...
                break
            #TODO: inter-try delay
        #TODO: return radio to state it was before receiver (e.g. standby) - radio needs a pop() on this too?

        if payload == None: # nothing received in timeout
            return (None, None, None) # (radio_measurements, address, payload) #TODO: might be measurements, average min max?

        #TODO: extract addresses: header_manufacturerid, header_productid header_deviceid -> (m, p, d)
        m, p, d = None, None, None
        radio_measurements = None #TODO: get from radio.receive()
        address = (m, p, d)
        return (radio_measurements, address, payload)


class TwoBitAirInterface():
    def __init__(self):
        self.radio = radio # aids mocking later

        class RadioDefaults():
            frequency     = 433.92
            modulation    = radio.RADIO_MODULATION_OOK

        class TxDefaults(RadioDefaults):
            power_level   = 0
            inner_times   = 8
            outer_delay   = 0
            outer_times   = 1
        self.tx_defaults = TxDefaults()

        class RxDefaults(RadioDefaults):
            poll_rate     = 100  #ms
            timeout       = 1000 #ms
        self.rx_defaults = RxDefaults()

    ##@log_method
    def send(self, payload, radio_config=None):
        #   payload is just a list of bytes, or a byte buffer
        #   radio_config is an overlay on top of radio tx defaults

        house_address = payload["house_address"]
        device_index  = payload["device_index"]
        state         = payload["on"]
        bytes = TwoBit.encode_switch_message(state, device_index, house_address)
        radio.modulation(ook=True)

        # Set radio defaults, if no override
        outer_times = self.tx_defaults.outer_times
        outer_delay = self.tx_defaults.outer_delay
        inner_times = self.tx_defaults.inner_times

        # Merge any wanted radio params, if provided
        if radio_config != None:
            try:
                outer_times = radio_config.outer_times
            except AttributeError: pass
            try:
                outer_delay = radio_config.outer_delay
            except AttributeError: pass
            try:
                inner_times = radio_config.inner_times
            except AttributeError: pass

        ##print("inner times %s" % inner_times)
        radio.transmit(bytes, outer_times=outer_times, inner_times=inner_times, outer_delay=outer_delay)
        # radio auto-pops to state before transmit

    ##@log_method
    def receive(self, radio_config=None): # -> (radio_measurements, address or None, payload or None)
        #   radio_params is an overlay on top of radio rx defaults (e.g. poll rate, timeout, min payload, max payload)
        #   radio_measurements might include rssi reading, short payload report, etc
        #TODO: merge radio_params with self.tx_defaults
        #TODO: configure radio modulation based on merged params

        #TODO: poll radio at rate until timeout or received
        #TODO: start timeout timer
        payload = None
        radio.receiver(ook=True)
        while True: # timer not expired
            if radio.is_receive_waiting():
                #TODO: radio config should set receive preamble 4 bytes to prevent false triggers
                payload = radio.receive(size=12) #TODO: payload, radio_measurements = radio.receive()
                p = TwoBit.decode(payload)
                #TODO: if failure, report it, but keep trying
                #if  check passes...
                break
            #TODO: inter-try delay
        #TODO: return radio to state it was before receiver (e.g. standby) - radio needs a pop() on this too?

        if payload == None: # nothing received in timeout
            return (None, None, None) # (radio_measurements, address, payload) #TODO: might be measurements, average min max?

        #TODO: extract addresses (house_address, device_index)
        radio_measurements = None #TODO: return this from radio.receive()
        h = 0xC8C8C #TODO: Get house address from TwoBit.decode()[:10]
        d = 0xEE    #TODO: Get device command from TwoBit.decode()[11:12]
        address = (h, d)
        return (radio_measurements, address, payload)


# END


