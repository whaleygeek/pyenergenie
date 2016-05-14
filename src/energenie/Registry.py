# Registry.py  14/05/2016  D.J.Whale
#
# A simple registry of connected devices.
#
# NOTE: This is an initial, non persisted implementation only

import time
import Devices

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


def size():
    return len(directory)


def get_sensorids():
    return directory.keys()


def get_info(sensor_id):
    return directory[sensor_id]

# END
