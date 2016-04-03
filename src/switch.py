# switch.py  17/03/2016  D.J.Whale
#
# Control Energenie switches.
# Note, at the moment, this only works with MiHome Adaptor Plus devices
# because the 'sensorid' is discovered via the monitor message.
# You could probably fake it by preloading the directory with your sensorid
# if you know what it is.

# Note, this is *only* a test program, to exercise the lower level code.
# Don't expect this to be a good starting point for an application.
# Consider waiting for me to finish developing the device object interface first.

import time

from energenie import OpenThings
from energenie import Devices, Messages, radio
from Timer import Timer

# Increase this if you have lots of switches, so that the receiver has enough
# time to receive update messages, otherwise your devices won't make it into
# the device directory.
TX_RATE = 10 # seconds between each switch change cycle

def warning(msg):
    print("warning:%s" % str(msg))

def trace(msg):
    print("monitor:%s" % str(msg))


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


def send_join_ack(mfrid, productid, sensorid):
    # send back a JOIN ACK, so that join light stops flashing
    response = OpenThings.alterMessage(Messages.JOIN_ACK,
        header_mfrid=mfrid,
        header_productid=productid,
        header_sensorid=sensorid)
    p = OpenThings.encode(response)
    radio.transmitter()
    radio.transmit(p)
    radio.receiver()


def switch_loop():
    """Listen to sensor messages, and turn switches on and off every few seconds"""

    # Define the schedule of message polling
    sendSwitchTimer    = Timer(TX_RATE, 1)   # every n seconds offset by initial 1
    switch_state       = 0             # OFF
    radio.receiver()

    while True:
        # See if there is a payload, and if there is, process it
        if radio.isReceiveWaiting():
            #trace("receiving payload")
            payload = radio.receive()
            try:
                decoded = OpenThings.decode(payload)
            except OpenThings.OpenThingsException as e:
                warning("Can't decode payload:" + str(e))
                continue
                      
            OpenThings.showMessage(decoded)
            # Any device that reports will be added to the non-persistent directory
            updateDirectory(decoded)
            #trace(decoded)

            # Process any JOIN messages by sending back a JOIN-ACK to turn the LED off
            if len(decoded["recs"]) == 0:
                # handle messages with zero recs in them silently
                print("Empty record:%s" % decoded)
            else:
                # assume only 1 rec in a join, for now
                #TODO: use OpenThings.getFromMessage("header_mfrid")
                if decoded["recs"][0]["paramid"] == OpenThings.PARAM_JOIN:
                    header    = decoded["header"]
                    mfrid     = header["mfrid"]
                    productid = header["productid"]
                    sensorid  = header["sensorid"]
                    send_join_ack(mfrid, productid, sensorid)


        # Toggle the switch on all devices in the directory
        if len(directory) > 0 and sendSwitchTimer.check():
            print("transmit")
            radio.transmitter()

            for sensorid in directory.keys():
                # Only try to toggle the switch for devices that actually have a switch
                header = directory[sensorid]["header"]
                mfrid = header["mfrid"]
                productid = header["productid"]

                if Devices.hasSwitch(mfrid, productid):
                    request = OpenThings.alterMessage(Messages.SWITCH,
                        header_sensorid=sensorid,
                        recs_0_value=switch_state)
                    p = OpenThings.encode(request)
                    print("Sending switch message to %s %s" % (hex(productid), hex(sensorid)))
                    # Transmit multiple times, hope one of them gets through
                    for i in range(4):
                        radio.transmit(p)

            radio.receiver()
            print("receive")
            switch_state = (switch_state+1) % 2 # toggle
        

if __name__ == "__main__":
    
    trace("starting switch tester")
    radio.init()
    OpenThings.init(Devices.CRYPT_PID)

    try:
        switch_loop()

    finally:
        radio.finished()

# END
