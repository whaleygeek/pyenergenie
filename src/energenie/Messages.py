# Message.py  03/04/2015  D.J.Whale
#
# pydict formatted message structures for OpenThings

try: # python 2
    import Devices
    import OpenThings
except ImportError:
    from . import Devices
    from . import OpenThings

SWITCH = {
    "header": {
        "mfrid":       Devices.MFRID,
        "productid":   Devices.PRODUCTID_MIHO005,
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


REGISTERED_SENSOR = {
    "header": {
        "mfrid":       0, # FILL IN
        "productid":   0, # FILL IN
        "encryptPIP":  Devices.CRYPT_PIP,
        "sensorid":    0 # FILL IN
    }
}


def send_join_ack(radio, mfrid, productid, sensorid):
    # send back a JOIN ACK, so that join light stops flashing
    response = OpenThings.alterMessage(JOIN_ACK,
        header_mfrid=mfrid,
        header_productid=productid,
        header_sensorid=sensorid)
    p = OpenThings.encode(response)
    radio.transmitter()
    radio.transmit(p, inner_times=2)
    radio.receiver()


# END
