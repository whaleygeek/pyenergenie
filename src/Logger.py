# Logger.py  14/05/2016  D.J.Whale
#
# A simple logger - logs to file.


from energenie import OpenThings
import os, time

LOG_FILENAME = "energenie.csv"
HEADINGS = 'timestamp,mfrid,prodid,sensorid,flags,switch,voltage,freq,reactive,real,apparent,current,temperature'


log_file = None

def trace(msg):
    print(str(msg))


def logMessage(msg):
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
    flags = [0 for i in range(8)]
    switch = None
    voltage = None
    freq = None
    reactive = None
    real = None
    apparent = None
    current = None
    temperature = None

    # capture any data that we want
    ##trace(msg)
    for rec in msg['recs']:
        paramid = rec['paramid']
        try:
            value = rec['value']
        except:
            value = None

        if   paramid == OpenThings.PARAM_SWITCH_STATE:
            switch = value
            flags[0] = 1
        elif paramid == OpenThings.PARAM_VOLTAGE:
            flags[1] = 1
            voltage = value
        elif paramid == OpenThings.PARAM_FREQUENCY:
            flags[2] = 1
            freq = value
        elif paramid == OpenThings.PARAM_REACTIVE_POWER:
            flags[3] = 1
            reactive = value
        elif paramid == OpenThings.PARAM_REAL_POWER:
            flags[4] = 1
            real = value
        elif paramid == OpenThings.PARAM_APPARENT_POWER:
            flags[5] = 1
            apparent = value
        elif paramid == OpenThings.PARAM_CURRENT:
            flags[6] = 1
            current = value
        elif paramid == OpenThings.PARAM_TEMPERATURE:
            flags[7] = 1
            temperature = value

    # generate a line of CSV
    flags = "".join([str(a) for a in flags])
    csv = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (timestamp, mfrid, productid, sensorid, flags, switch, voltage, freq, reactive, real, apparent, current, temperature)
    log_file.write(csv + '\n')
    log_file.flush()
    ##trace(csv) # testing

# END
