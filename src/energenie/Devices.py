# Devices.py  30/09/2015  D.J.Whale
#
# Information about specific Energenie devices
# This table is mostly reverse-engineered from various websites and web catalogues.

MFRID                            = 0x04

# Deprecated, these are old device names, do not use.
#PRODUCTID_C1_MONITOR             = 0x01   # MIHO004 Monitor
#PRODUCTID_R1_MONITOR_AND_CONTROL = 0x02   # MIHO005 Adaptor Plus

#PRODUCTID_MIHO001               =        #         Home Hub
#PRODUCTID_MIHO002               =        #         Control only (Uses Legacy OOK protocol)
#PRODUCTID_MIHO003               = 0x0?   #         Hand Controller
PRODUCTID_MIHO004                = 0x01   #         Monitor only
PRODUCTID_MIHO005                = 0x02   #         Adaptor Plus
PRODUCTID_MIHO006                = 0x05   #         House Monitor
#PRODUCTID_MIHO007               = 0x0?   #         Double Wall Socket White
#PRODUCTID_MIHO008               = 0x0?   #         Single light switch
#PRODUCTID_MIHO009 not used
#PRODUCTID_MIHO010 not used
#PRODUCTID_MIHO011 not used
#PRODUCTID_MIHO012 not used
PRODUCTID_MIHO013                = 0x03   #         eTRV
#PRODUCTID_MIHO014               = 0x0?   #         In-line Relay
#PRODUCTID_MIHO015 not used
#PRODUCTID_MIHO016 not used
#PRODUCTID_MIHO017
#PRODUCTID_MIHO018
#PRODUCTID_MIHO019
#PRODUCTID_MIHO020
#PRODUCTID_MIHO021               = 0x0?   #         Double Wall Socket Nickel
#PRODUCTID_MIHO022               = 0x0?   #         Double Wall Socket Chrome
#PRODUCTID_MIHO023               = 0x0?   #         Double Wall Socket Brushed Steel
#PRODUCTID_MIHO024               = 0x0?   #         Style Light Nickel
#PRODUCTID_MIHO025               = 0x0?   #         Style Light Chrome
#PRODUCTID_MIHO026               = 0x0?   #         Style Light Steel
#PRODUCTID_MIHO027 starter pack bundle
#PRODUCTID_MIHO028 eco starter pack
#PRODUCTID_MIHO029 heating bundle
#PRODUCTID_MIHO030 not used
#PRODUCTID_MIHO031 not used
#PRODUCTID_MIHO032 not used
#PRODUCTID_MIHO033 not used
#PRODUCTID_MIHO034 not used
#PRODUCTID_MIHO035 not used
#PRODUCTID_MIHO036 not used
#PRODUCTID_MIHO037 Adaptor Plus Bundle
#PRODUCTID_MIHO038 2-gang socket Bundle
#PRODUCTID_MIHO039 2-gang socket Bundle black nickel
#PRODUCTID_MIHO040 2-gang socket Bundle chrome
#PRODUCTID_MIHO041 2-gang socket Bundle stainless steel


CRYPT_PID                        = 242
CRYPT_PIP                        = 0x0100

# OpenThings does not support a broadcast id,
# but Energenie added one for their MiHome Adaptors.
# This makes simple discovery possible.
BROADCAST_ID                     = 0xFFFFFF # Energenie broadcast

#TODO: put additional products in here from the Energenie directory
#TODO: make this table based

def getDescription(mfrid, productid):
    if mfrid == MFRID:
        mfr = "Energenie"
        if productid == PRODUCTID_MIHO004:
            product = "MIHO004 MONITOR"
        elif productid == PRODUCTID_MIHO005:
            product = "MIHO005 ADAPTOR PLUS"
        elif productid == PRODUCTID_MIHO006:
            product = "MIHO006 HOUSE MONITOR"
        elif productid == PRODUCTID_MIHO013:
            product = "MIHO013 ETRV"
        else:
            product = "UNKNOWN_%s" % str(hex(productid))
    else:
        mfr     = "UNKNOWN_%s" % str(hex(mfrid))
        product = "UNKNOWN_%s" % str(hex(productid))

    return "Manufacturer:%s Product:%s" % (mfr, product)


def hasSwitch(mfrid, productid):
    if mfrid != MFRID:                  return False
    if productid == PRODUCTID_MIHO005:  return True
    return False


# END
