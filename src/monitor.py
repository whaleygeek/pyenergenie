# monitor.py  27/09/2015  D.J.Whale
#
# Monitor Energine MiHome plugs

# Note, this is *only* a test program, to exercise the lower level code.
# Don't expect this to be a good starting point for an application.
# Consider waiting for me to finish developing the device object interface first.
#
# However, it will log all messages from MiHome monitor, adaptor plus and house monitor
# to a CSV log file, so could be the basis for a non-controlling energy logging app.

import time

from energenie import OpenHEMS, Devices
from energenie import radio
from Timer import Timer
import os

LOG_FILENAME = "energenie.csv"

def warning(msg):
    print("warning:%s" % str(msg))

def trace(msg):
    print("monitor:%s" % str(msg))

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
    flags = [0 for i in range(7)]
    switch = None
    voltage = None
    freq = None
    reactive = None
    real = None
    apparent = None
    current = None

    # capture any data that we want
    #print(msg)
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
        elif paramid == OpenHEMS.PARAM_APPARENT_POWER:
            flags[5] = 1
            apparent = value
        elif paramid == OpenHEMS.PARAM_CURRENT:
            flags[6] = 1
            current = value

    # generate a line of CSV
    flags = "".join([str(a) for a in flags])
    csv = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (timestamp, mfrid, productid, sensorid, flags, switch, voltage, freq, reactive, real, apparent, current)
    log_file.write(csv + '\n')
    log_file.flush()
    trace(csv) # testing


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
        #trace(allkeys(directory))

    directory[sensorId]["time"] = now
    #TODO would be good to keep recs, but need to iterate through all and key by paramid,
    #not as a list index, else merging will be hard.


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

def send_join_ack(mfrid, productid, sensorid):
    # send back a JOIN ACK, so that join light stops flashing
    response = OpenHEMS.alterMessage(JOIN_ACK_MESSAGE,
        header_mfrid=mfrid,
        header_productid=productid,
        header_sensorid=sensorid)
    p = OpenHEMS.encode(response)
    radio.transmitter()
    radio.transmit(p)
    radio.receiver()


def monitor_loop():
    """Capture any incoming messages and log to CSV file"""

    radio.receiver()

    while True:
        # See if there is a payload, and if there is, process it
        if radio.isReceiveWaiting():
            #trace("receiving payload")
            payload = radio.receive()
            try:
                decoded = OpenHEMS.decode(payload)
            except OpenHEMS.OpenHEMSException as e:
                warning("Can't decode payload:" + str(e))
                continue
                      
            OpenHEMS.showMessage(decoded)
            # Any device that reports will be added to the non-persistent directory
            updateDirectory(decoded)
            #trace(decoded)
            logMessage(decoded)

            # Process any JOIN messages by sending back a JOIN-ACK to turn the LED off
            if len(decoded["recs"]) == 0:
                # handle messages with zero recs in them silently
                print("Empty record:%s" % decoded)
            else:
                # assume only 1 rec in a join, for now
                #TODO: write OpenHEMS.getFromMessage("header_mfrid")
                if decoded["recs"][0]["paramid"] == OpenHEMS.PARAM_JOIN:
                    header    = decoded["header"]
                    mfrid     = header["mfrid"]
                    productid = header["productid"]
                    sensorid  = header["sensorid"]
                    send_join_ack(mfrid, productid, sensorid)



if __name__ == "__main__":
    
    trace("starting monitor tester")
    radio.init()
    OpenHEMS.init(Devices.CRYPT_PID)

    try:
        monitor_loop()

    finally:
        radio.finished()

# END
