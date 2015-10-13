# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices

MFRID                            = 0x04
PRODUCTID_C1_MONITOR             = 0x01
PRODUCTID_R1_MONITOR_AND_CONTROL = 0x02
PRODUCTID_ETRV                   = 0x03
CRYPT_PID                        = 242
CRYPT_PIP                        = 0x0100

# OpenHEMS does not support a broadcast id, but Energine added one for their
# MiHome Adaptors. This makes simple discovery possible.
BROADCAST_ID                     = 0xFFFFFF # energenie broadcast

# TODO put additional products in here from the Energenie directory

def getDescription(mfrid, productid):
    if mfrid == MFRID:
        mfr = "Energenie"
        if productid == PRODUCTID_C1_MONITOR:
            product = "C1 MONITOR"
        elif productid == PRODUCTID_R1_MONITOR_AND_CONTROL:
            product = "R1 MONITOR/CONTROL"
        elif productid == PRODUCTID_ETRV:
            product = "eTRV"
        else:
            product = "UNKNOWN"
    else:
        mfr     = "UNKNOWN"
        product = "UNKNOWN"

    return "Manufactuer:%s Product:%s" % (mfr, product)


# END
