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

    # tx, pydict payload and radio params in
    # OpenThings encode and encrypt, configure radio for FSK transmit, pass repeats
    
    # rx, configure radio for FSK receive OpenThings decode and decrypt,
    # pydict payload and metadata (RSSI etc) out


class TwoBitAirInterface():
    pass
    # tx, pydict payload and radio params in
    # TwoBit encode, configure radio for OOK transmit, pass repeats

    # rx, configure radio for OOK receive, TwoBit decide
    # pydict payload and metadata (RSSI etc) out


# END


