'''
Created on 15 Oct 2015

@author: ed
'''
from energenie import Devices, OpenHEMS

MESSAGE_SWITCH = {
    "header": {
        "mfrid":       Devices.MFRID_ENERGENIE,
        "productid":   Devices.PRODUCTID_R1_MONITOR_AND_CONTROL,
        "encryptPIP":  Devices.CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      True,
            "paramid": OpenHEMS.PARAM_SWITCH_STATE,
            "typeid":  OpenHEMS.Value.UINT,
            "length":  1,
            "value":   0 # FILL IN
        }
    ]
}

MESSAGE_JOIN_ACK = {
    "header": {
        "mfrid":       0, # FILL IN
        "productid":   0, # FILL IN
        "encryptPIP":  Devices.CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      False,
            "paramid": OpenHEMS.PARAM_JOIN,
            "typeid":  OpenHEMS.Value.UINT,
            "length":  0
        }
    ]
}

MESSAGE_ETRV_SEND_BATTERY_LEVEL = {
    "header": {
        "mfrid":       Devices.MFRID_ENERGENIE,
        "productid":   Devices.PRODUCTID_ETRV,
        "encryptPIP":  Devices.CRYPT_PIP,
        "sensorid":    0 # FILL IN
    },
    "recs": [
        {
            "wr":      False,
            "paramid": OpenHEMS.PARAM_VOLTAGE,
            "typeid":  OpenHEMS.Value.UINT,
            "length":  0
        }
    ]
}
