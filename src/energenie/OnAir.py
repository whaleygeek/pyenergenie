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

class OpenThingsAirInterface():
    pass

    # init
    #   radio params defaults FSK, inner_repeats, outer_delay, outer_repeats, power_level, frequency

    # send(payload, radio_params)
    #   payload is a pydict suitable for OpenThings
    #   radio_params is an overlay on top of radio tx defaults
    #   tx, pydict payload and radio params in
    #   OpenThings encode and encrypt, configure radio for FSK transmit, pass repeats

    # receive(radio_params) #-> (radio_measurements) or (radio_measurements, payload)
    #   radio_params is an overlay on top of radio rx defaults (e.g. poll rate, timeout, min payload, max payload)
    #   radio_measurements might include rssi reading, short payload report, etc
    #   rx, configure radio for FSK receive OpenThings decode and decrypt,
    #   pydict payload and metadata (RSSI etc) out


class TwoBitAirInterface():
    pass

    # init
    #   radio params defaults OOK, inner_repeats, outer_delay, outer_repeats, power_level, frequency

    # send(payload, radio_params)
    #   payload is just a list of bytes, or a byte buffer
    #   radio_params is an overlay on top of radio tx defaults
    #   tx, pydict payload and radio params in
    #   TwoBit encode, configure radio for OOK transmit, pass repeats

    # receive(radio_params) #-> (radio_measurements) or (radio_measurements, payload)
    #   radio_params is an overlay on top of radio rx defaults (e.g. poll rate, timeout, min payload, max payload)
    #   radio_measurements might include rssi reading, short payload report, etc
    #   rx, configure radio for OOK receive, TwoBit decode
    #   pydict payload and metadata (RSSI etc) out


# END


