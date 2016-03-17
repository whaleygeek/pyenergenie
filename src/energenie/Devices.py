# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices

MFRID                            = 0x04

#PRODUCTID_MIHO001               = 0x0?   #         Home Hub
#PRODUCTID_MIHO002               = 0x0?   #         Control only
#PRODUCTID_MIHO003               = 0x0?   #         Hand Controller
PRODUCTID_C1_MONITOR             = 0x01   # MIHO004 Monitor
PRODUCTID_R1_MONITOR_AND_CONTROL = 0x02   # MIHO005 Adaptor Plus
PRODUCTID_MIHO006                = 0x05   #         House Monitor
#PRODUCTID_MIHO007               = 0x0?   #         Double Wall Socket White
#PRODUCTID_MIHO008               = 0x0?   #         Single light switch
#009 not used
#010 not used
#011 not used
#012 not used
PRODUCTID_MIHO013                = 0x03   #         eTRV
#PRODUCTID_MIHO014               = 0x0?   #         In-line Relay
#015 not used
#016 not used
#017
#018
#019
#020
#PRODUCTID_MIHO021               = 0x0?   #         Double Wall Socket Nickel
#PRODUCTID_MIHO022               = 0x0?   #         Double Wall Socket Chrome
#PRODUCTID_MIHO023               = 0x0?   #         Double Wall Socket Brushed Steel
#PRODUCTID_MIHO024               = 0x0?   #         Style Light Nickel
#PRODUCTID_MIHO025               = 0x0?   #         Style Light Chrome
#PRODUCTID_MIHO026               = 0x0?   #         Style Light Steel
#027 starter pack bundle
#028 eco starter pack
#029 heating bundle
#030-036 not used
#037 Adaptor Plus Bundle
#038 2-gang socket Bundle
#039 2-gang socket Bundle black nickel
#040 2-gang socket Bundle chrome
#041 2-gang socket Bundle stainless steel


CRYPT_PID                        = 242
CRYPT_PIP                        = 0x0100

# OpenHEMS does not support a broadcast id, but Energenie added one for their
# MiHome Adaptors. This makes simple discovery possible.
BROADCAST_ID                     = 0xFFFFFF # energenie broadcast

# TODO put additional products in here from the Energenie directory
# TODO make this table based

def getDescription(mfrid, productid):
    if mfrid == MFRID:
        mfr = "Energenie"
        if productid == PRODUCTID_C1_MONITOR:
            product = "C1 MONITOR"
        elif productid == PRODUCTID_R1_MONITOR_AND_CONTROL:
            product = "MIHO005 ADAPTOR PLUS"
        elif productid == PRODUCTID_MIHO006:
            product = "MIHO006 HOUSE MONITOR"
        elif productid == PRODUCTID_MIHO013:
            product = "MIHO013 ETRV"
        else:
            product = "UNKNOWN"
    else:
        mfr     = "UNKNOWN"
        product = "UNKNOWN"

    return "Manufacturer:%s Product:%s" % (mfr, product)


def hasSwitch(mfrid, productid):
    if mfrid != MFRID:                                return False
    if productid == PRODUCTID_R1_MONITOR_AND_CONTROL: return True
    return False


# END
