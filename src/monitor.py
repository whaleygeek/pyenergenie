# monitor.py  27/09/2015  D.J.Whale
#
# Monitor settings of Energine MiHome plugs

import time

from energenie import OpenHEMS, Devices
from energenie import radio
from Timer import Timer
import os

LOG_FILENAME = "energenie.csv"

def trace(msg):
    print(str(msg))

log_file = None

def logMessage (msg):
    HEADINGS = 'timestamp,mfrid,prodid,sensorid,flags,switch,voltage,freq,reactive,real'

    global log_file
    if log_file == None:
        if not os.path.isfile(LOG_FILENAME):
            log_file = open(LOG_FILENAME, 'w')
            log_file.write(HEADINGS + '\n')
        else:
            log_file = open(LOG_FILENAME, 'a') # append

    # get the header
    header    = msg['header']
    timestamp = time.time()
    mfrid     = header['mfrid']
    productid = header['productid']
    sensorid  = header['sensorid']

    # set defaults for any data that doesn't appear in this message
    # but build flags so we know which ones this contains
    flags = [0,0,0,0,0]
    switch = None
    voltage = None
    freq = None
    reactive = None
    real = None

    # capture any data that we want
    for rec in msg['recs']:
        paramid = rec['paramid']
        try:
            value = rec['value']
        except:
            value = None
            
        if   paramid == OpenHEMS.PARAM_SWITCH_STATE:
            switch = value
            flags[0] = 1
        elif paramid == OpenHEMS.PARAM_VOLTAGE:
            flags[1] = 1
            voltage = value
        elif paramid == OpenHEMS.PARAM_FREQUENCY:
            flags[2] = 1
            freq = value
        elif paramid == OpenHEMS.PARAM_REACTIVE_POWER:
            flags[3] = 1
            reactive = value
        elif paramid == OpenHEMS.PARAM_REAL_POWER:
            flags[4] = 1
            real = value

    # generate a line of CSV
    flags = "".join([str(a) for a in flags])
    csv = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (timestamp, mfrid, productid, sensorid, flags, switch, voltage, freq, reactive, real)
    log_file.write(csv + '\n')
    log_file.flush()
    print(csv) # testing


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
    sendSwitchTimer    = Timer(60, 1)   # every n seconds offset by initial 1
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
            logMessage(decoded)
            
            #TODO: Should remember report time of each device,
            #and reschedule command messages to avoid their transmit slot
            #making it less likely to miss an incoming message due to
            #the radio being in transmit mode

            # assume only 1 rec in a join, for now
            if len(decoded["recs"])>0 and decoded["recs"][0]["paramid"] == OpenHEMS.PARAM_JOIN:
                #TODO: write OpenHEMS.getFromMessage("header_mfrid")
                response = OpenHEMS.alterMessage(JOIN_ACK_MESSAGE,
                    header_mfrid=decoded["header"]["mfrid"],
                    header_productid=decoded["header"]["productid"],
                    header_sensorid=decoded["header"]["sensorid"])
                p = OpenHEMS.encode(response)
                radio.transmitter()
                radio.transmit(p)
                radio.receiver()

        if sendSwitchTimer.check() and decoded != None and decoded["header"]["productid"] in [Devices.PRODUCTID_C1_MONITOR, Devices.PRODUCTID_R1_MONITOR_AND_CONTROL]:
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
