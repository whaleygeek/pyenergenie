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

import OpenThings
import TwoBit
import radio


class OpenThingsAirInterface():
    def __init__(self):
        self.radio = radio # aids mocking later
        #TODO: tx defaults
        # FSK, inner_repeats, outer_delay, outer_repeats, power_level, frequency
        #TODO: rx defaults
        # FSK, poll_rate, timeout, frequency

    def send(self, payload, radio_params=None):
        #   payload is a pydict suitable for OpenThings
        #   radio_params is an overlay on top of radio tx defaults
        #   tx, pydict payload and radio params in
        pass #TODO
        #TODO: OpenThings.encode()
        #TODO: configure radio modulation
        #TODO: set radio to transmit mode
        #TODO: configure other radio parameters
        #TODO: transmit payload
        #TODO: return radio to state before transmit

    def receive(self, radio_params): # -> (radio_measurements, address or None, payload or None)
        #   radio_params is an overlay on top of radio rx defaults (e.g. poll rate, timeout, min payload, max payload)
        #   radio_measurements might include rssi reading, short payload report, etc
        #   rx, configure radio for FSK receive OpenThings decode and decrypt,
        #   pydict payload and metadata (RSSI etc) out
        pass # TODO
        #TODO: configure radio modulation
        #TODO: set radio to receive mode
        #TODO: set other radio parameters
        #TODO: poll radio at rate until timeout or received
        #TODO: return radio to state it was before receive
        #TODO: OpenThings.decode
        #TODO: report damaged payload (crc failure)
        #TODO: extract addresses
        #TODO: return (radio_measurements, address, payload)


class TwoBitAirInterface():
    def __init__(self):
        self.radio = radio # aids mocking later
        #TODO: tx defaults
        # OOK, inner_repeats, outer_delay, outer_repeats, power_level, frequency
        #TODO: rx defaults
        # OOK, poll_rate, timeout, frequency

    def send(self, payload, radio_params=None):
        #   payload is just a list of bytes, or a byte buffer
        #   radio_params is an overlay on top of radio tx defaults
        #   tx, pydict payload and radio params in
        #   TwoBit encode, configure radio for OOK transmit, pass repeats
        pass #TODO

        #TODO: TwoBit.encode()
        #TODO: configure radio modulation
        #TODO: set radio to transmit mode
        #TODO: configure other radio parameters
        #TODO: transmit payload
        #TODO: return radio to state before transmit

    def receive(self, radio_params): # -> (radio_measurements, address or None, payload or None)
        #   radio_params is an overlay on top of radio rx defaults (e.g. poll rate, timeout, min payload, max payload)
        #   radio_measurements might include rssi reading, short payload report, etc
        #   rx, configure radio for OOK receive, TwoBit decode
        #   pydict payload and metadata (RSSI etc) out
        pass # TODO
        #TODO: configure radio modulation
        #TODO: set radio to receive mode
        #TODO: set other radio parameters
        #TODO: poll radio at rate until timeout or received
        #TODO: return radio to state it was before receive
        #TODO: TwoBit.decode
        #TODO: report damaged payload??
        #TODO: extract addresses (house_address, device_index)
        #TODO: return (radio_measurements, address, payload)


# END


