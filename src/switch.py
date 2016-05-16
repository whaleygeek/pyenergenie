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
from energenie import Devices, Messages, Registry, OpenThings, radio
from Timer import Timer


# Increase this if you have lots of switches, so that the receiver has enough
# time to receive update messages, otherwise your devices won't make it into
# the device directory.
TX_RATE = 2 # seconds between each switch change cycle


def warning(msg):
    print("warning:%s" % str(msg))


def trace(msg):
    print("monitor:%s" % str(msg))


#----- TEST APPLICATION -------------------------------------------------------

def switch_sniff_loop():
    """Listen to sensor messages and add them to the Registry"""

    # See if there is a payload, and if there is, process it
    if radio.is_receive_waiting():
        ##trace("receiving payload")
        payload = radio.receive()
        try:
            decoded = OpenThings.decode(payload)
            now = time.time()
        except OpenThings.OpenThingsException as e:
            warning("Can't decode payload:" + str(e))
            return

        OpenThings.showMessage(decoded, timestamp=now)
        # Any device that reports will be added to the non-persistent directory
        Registry.update(decoded)
        ##trace(decoded)

        # Process any JOIN messages by sending back a JOIN-ACK to turn the LED off
        if len(decoded["recs"]) == 0:
            # handle messages with zero recs in them silently
            print("Empty record:%s" % decoded)
        else:
            # assume only 1 rec in a join, for now
            if decoded["recs"][0]["paramid"] == OpenThings.PARAM_JOIN:
                mfrid     = OpenThings.getFromMessage(decoded, "header_mfrid")
                productid = OpenThings.getFromMessage(decoded, "header_productid")
                sensorid  = OpenThings.getFromMessage(decoded, "header_sensorid")
                Messages.send_join_ack(radio, mfrid, productid, sensorid)


def switch_toggle_loop():
    """Toggle the switch on all devices in the directory"""

    global switch_state

    if Registry.size() > 0 and sendSwitchTimer.check():
        print("transmit")
        radio.transmitter()

        for sensorid in Registry.get_sensorids():
            # Only try to toggle the switch for devices that actually have a switch
            header = Registry.get_info(sensorid)["header"]
            mfrid = header["mfrid"]
            productid = header["productid"]

            if Devices.hasSwitch(mfrid, productid):
                request = OpenThings.alterMessage(Messages.SWITCH,
                    header_sensorid=sensorid,
                    recs_0_value=switch_state)
                p = OpenThings.encode(request)
                print("Sending switch message to %s %s" % (hex(productid), hex(sensorid)))
                # Transmit multiple times, hope one of them gets through
                radio.transmit(p, inner_times=2)

        radio.receiver()
        switch_state = (switch_state+1) % 2 # toggle
        

if __name__ == "__main__":
    
    trace("starting switch tester")
    radio.init()
    OpenThings.init(Devices.CRYPT_PID)

    # Seed the registry with a known device, to simplify tx-only testing
    SENSOR_ID = 0x68B # captured from a real device
    device_header = OpenThings.alterMessage(Messages.REGISTERED_SENSOR,
        header_mfrid     = Devices.MFRID,
        header_productid = Devices.PRODUCTID_MIHO005, # adaptor plus
        header_sensorid  = SENSOR_ID)
    Registry.update(device_header)


    sendSwitchTimer    = Timer(TX_RATE, 1)   # every n seconds offset by initial 1
    switch_state       = 0 # OFF
    radio.receiver()

    try:
        while True:
            switch_sniff_loop()
            switch_toggle_loop()

    finally:
        radio.finished()

# END
