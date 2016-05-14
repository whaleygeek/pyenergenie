# Message.py  03/04/2015  D.J.Whale
#
# pydict formatted message structures for OpenThings

import Devices
import OpenThings

SWITCH = {
    "header": {
        "mfrid":       Devices.MFRID,
        "productid":   Devices.PRODUCTID_R1_MONITOR_AND_CONTROL,
        "encryptPIP":  Devices.CRYPT_PIP,
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
        "encryptPIP":  Devices.CRYPT_PIP,
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


def send_join_ack(radio, mfrid, productid, sensorid):
    # send back a JOIN ACK, so that join light stops flashing
    response = OpenThings.alterMessage(JOIN_ACK,
        header_mfrid=mfrid,
        header_productid=productid,
        header_sensorid=sensorid)
    p = OpenThings.encode(response)
    radio.transmitter()
    radio.transmit(p)
    radio.receiver()


# END
