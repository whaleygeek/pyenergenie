# monitor.py  27/09/2015  D.J.Whale
#
# Monitor settings of Energine MiHome plugs

import time

from energenie import OpenHEMS, Devices
from energenie import radio
from Timer import Timer

def trace(msg):
    print(str(msg))


#----- TEST APPLICATION -------------------------------------------------------

directory = {}

def allkeys(d):
    result = ""
    for k in d:
        if len(result) != 0:
            result += ','
        result += str(k)
    return result

        
def updateDirectory(message):
    """Update the local directory with information about this device"""
    now      = time.time()
    header   = message["header"]
    sensorId = header["sensorid"]

    if not directory.has_key(sensorId):
        # new device discovered
        desc = Devices.getDescription(header["mfrid"], header["productid"])
        print("ADD device:%s %s" % (hex(sensorId), desc))
        directory[sensorId] = {"header": message["header"]}
        print(allkeys(directory))

    directory[sensorId]["time"] = now
    #TODO would be good to keep recs, but need to iterate through all and key by paramid,
    #not as a list index, else merging will be hard.


SWITCH_MESSAGE = {
    "header": {
        "mfrid":       Devices.MFRID,
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


JOIN_ACK_MESSAGE = {
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



def monitor():
    """Send discovery and monitor messages, and capture any responses"""

    # Define the schedule of message polling
    sendSwitchTimer    = Timer(5, 1)   # every 5 seconds offset by initial 1
    switch_state       = 0             # OFF
    radio.receiver()
    decoded            = None

    while True:
        # See if there is a payload, and if there is, process it
        if radio.isReceiveWaiting():
            trace("receiving payload")
            payload = radio.receive()
            try:
                decoded = OpenHEMS.decode(payload)
            except OpenHEMS.OpenHEMSException as e:
                print("Can't decode payload:" + str(e))
                continue
                      
            OpenHEMS.showMessage(decoded)
            updateDirectory(decoded)
            #TODO: Should remember report time of each device,
            #and reschedule command messages to avoid their transmit slot
            #making it less likely to miss an incoming message due to
            #the radio being in transmit mode

            # assume only 1 rec in a join, for now
            if decoded["recs"][0]["paramid"] == OpenHEMS.PARAM_JOIN:
                #TODO: write OpenHEMS.getFromMessage("header_mfrid")
                response = OpenHEMS.alterMessage(JOIN_ACK_MESSAGE,
                    header_mfrid=decoded["header"]["mfrid"],
                    header_productid=decoded["header"]["productid"],
                    header_sensorid=decoded["header"]["sensorid"])
                p = OpenHEMS.encode(response)
                radio.transmitter()
                radio.transmit(p)
                radio.receiver()

        if sendSwitchTimer.check() and decoded != None:
            request = OpenHEMS.alterMessage(SWITCH_MESSAGE,
                header_sensorid=decoded["header"]["sensorid"],
                recs_0_value=switch_state)
            p = OpenHEMS.encode(request)
            radio.transmitter()
            radio.transmit(p)
            radio.receiver()
            switch_state = (switch_state+1) % 2 # toggle
        

if __name__ == "__main__":

    radio.init()
    OpenHEMS.init(Devices.CRYPT_PID)

    try:
        monitor()

    finally:
        radio.finished()

# END
