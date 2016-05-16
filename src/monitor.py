# monitor.py  27/09/2015  D.J.Whale
#
# Monitor Energine MiHome plugs

# Note, this is *only* a test program, to exercise the lower level code.
# Don't expect this to be a good starting point for an application.
# Consider waiting for me to finish developing the device object interface first.
#
# However, it will log all messages from MiHome monitor, adaptor plus and house monitor
# to a CSV log file, so could be the basis for a non-controlling energy logging app.

from energenie import Registry, Devices, Messages, OpenThings, radio
import time
import Logger

def warning(msg):
    print("warning:%s" % str(msg))


def trace(msg):
    print("monitor:%s" % str(msg))


#----- TEST APPLICATION -------------------------------------------------------

def monitor_loop():
    """Capture any incoming messages and log to CSV file"""

    radio.receiver()

    while True:
        # See if there is a payload, and if there is, process it
        if radio.is_receive_waiting():
            trace("receiving payload")
            payload = radio.receive()
            try:
                decoded = OpenThings.decode(payload)
                now = time.time()
            except OpenThings.OpenThingsException as e:
                warning("Can't decode payload:" + str(e))
                continue
                      
            OpenThings.showMessage(decoded, timestamp=now)
            # Any device that reports will be added to the non-persistent directory
            Registry.update(decoded)
            ##trace(decoded)
            Logger.logMessage(decoded)

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


if __name__ == "__main__":
    
    trace("starting monitor tester")
    radio.init()
    OpenThings.init(Devices.CRYPT_PID)

    try:
        monitor_loop()

    finally:
        radio.finished()

# END
