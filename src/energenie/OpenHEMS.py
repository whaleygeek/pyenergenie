# OpenHEMS.py  27/09/2015  D.J.Whale
#
# Implement OpenHEMS message encoding and decoding

import crypto

# report has bit 7 clear
# command has bit 7 set

PARAM_ALARM           = 0x21
PARAM_DEBUG_OUTPUT    = 0x2D
PARAM_IDENTIFY        = 0x3F
PARAM_SOURCE_SELECTOR = 0x40 # command only
PARAM_WATER_DETECTOR  = 0x41
PARAM_GLASS_BREAKAGE  = 0x42
PARAM_CLOSURES        = 0x43
PARAM_DOOR_BELL       = 0x44
PARAM_ENERGY          = 0x45
PARAM_FALL_SENSOR     = 0x46
PARAM_GAS_VOLUME      = 0x47
PARAM_AIR_PRESSURE    = 0x48
PARAM_ILLUMINANCE     = 0x49
PARAM_LEVEL           = 0x4C
PARAM_RAINFALL        = 0x4D
PARAM_APPARENT_POWER  = 0x50
PARAM_POWER_FACTOR    = 0x51
PARAM_REPORT_PERIOD   = 0x52
PARAM_SMOKE_DETECTOR  = 0x53
PARAM_TIME_AND_DATE   = 0x54
PARAM_VIBRATION       = 0x56
PARAM_WATER_VOLUME    = 0x57
PARAM_WIND_SPEED      = 0x58
PARAM_GAS_PRESSURE    = 0x61
PARAM_BATTERY_LEVEL   = 0x62
PARAM_CO_DETECTOR     = 0x63
PARAM_DOOR_SENSOR     = 0x64
PARAM_EMERGENCY       = 0x65
PARAM_FREQUENCY       = 0x66
PARAM_GAS_FLOW_RATE   = 0x67
PARAM_CURRENT         = 0x69
PARAM_JOIN            = 0x6A
PARAM_LIGHT_LEVEL     = 0x6C
PARAM_MOTION_DETECTOR = 0x6D
PARAM_OCCUPANCY       = 0x6F
PARAM_REAL_POWER      = 0x70
PARAM_REACTIVE_POWER  = 0x71
PARAM_ROTATION_SPEED  = 0x72
PARAM_SWITCH_STATE    = 0x73
PARAM_TEMPERATURE     = 0x74
PARAM_VOLTAGE         = 0x76
PARAM_WATER_FLOW_RATE = 0x77
PARAM_WATER_PRESSURE  = 0x78

PARAM_TEST            = 0xAA



crypt_pid = None
crypt_pip = None

def init(pid, pip):
    global crypt_pid, crypt_pip
    crypt_pid = pid
    crypt_pip = pip


def warning(msg):
    print("warning:" + str(msg))


#TODO decode OpenHEMS message payload structure
#TODO decrypt OpenHEMS message payload
#TODO check the CRC is correct

"""
		case S_MSGLEN:							// Read message length
		case S_MANUFACT_ID:						// Read manufacturer identifier
		case S_PRODUCT_ID:						// Read product identifier
		case S_ENCRYPTPIP:						// Read encryption pip
		case S_SENSORID:						// Read sensor ID
	    /******************* start reading RECORDS  ********************/
		case S_DATA_PARAMID:					// Read record parameter identifier
			msgPtr->paramId = msgPtr->value & 0x7F;
			temp = getIdName(msgPtr->paramId);
			printf(" %s=", temp);
			if (msgPtr->paramId == 0)			// Parameter identifier CRC. Go to CRC
			{
				msgPtr->state = S_CRC;
				msgPtr->recordBytesToRead = SIZE_CRC;
			}
			else
			{
				msgPtr->state = S_DATA_TYPEDESC;
				msgPtr->recordBytesToRead = SIZE_DATA_TYPEDESC;
			}
			if (strcmp(temp, "Unknown") == 0)	// Unknown parameter, finish fetching message
				msgPtr->state = S_FINISH;
			break;
		case S_DATA_TYPEDESC:					// Read record type description
			if ((msgPtr->value & 0x0F) == 0)	// No more data to read in that record
			{
				msgPtr->state = S_DATA_PARAMID;
				msgPtr->recordBytesToRead = SIZE_DATA_PARAMID;
			}
			else
			{
				msgPtr->state = S_DATA_VAL;
				msgPtr->recordBytesToRead = msgPtr->value & 0x0F;
			}
			msgPtr->type = msgPtr->value;
			break;
		case S_DATA_VAL:						// Read record data
			temp = getValString(msgPtr->value, msgPtr->type >> 4, msgPtr->recordBytesToRead);
			printf("%s", temp);
			msgPtr->state = S_DATA_PARAMID;
			msgPtr->recordBytesToRead = SIZE_DATA_PARAMID;
			if (strcmp(temp, "Reserved") == 0)
				msgPtr->state = S_FINISH;
			break;
	    /******************* finish reading RECORDS  ********************/
		case S_CRC:								// Check CRC
			msgPtr->state = S_FINISH;
			if ((int16_t)msgPtr->value == crc(msgPtr->buf + NON_CRC, msgPtr->bufCnt - NON_CRC - SIZE_CRC))
			{
				printf("OK\n");
			}
			else
			{
				printf("FAIL expVal=%04x, pip=%04x, val=%04x\n", (int16_t)msgPtr->value, msgPtr->pip, crc(msgPtr->buf + NON_CRC, msgPtr->bufCnt - NON_CRC - SIZE_CRC));
			}
			break;
"""

#TODO if can't decode message throw an exception
def decode(payload):
    buffer = ""
    length = payload[0]
    if length+1 != len(payload):
        warning("rx payload length mismatch")

    mfrId = payload[1]
    productId = payload[2]

    buffer += "len:" + str(length) + " "
    buffer += "mfr:" + hex(mfrId) + " "
    buffer += "prod:" + hex(productId) + " "

    pip = (payload[3]<<8) + payload[4]
    crypto.init(crypt_pid, pip)
    crypto.cryptPayload(payload, 5, len(payload)-5)

    for n in payload[5:]:
        buffer += hex(n) + " "

    #TODO check CRC matches
    return buffer


#----- MESSAGE ENCODER --------------------------------------------------------
#
# Encodes a message using the OpenHEMS message payload structure

# R1 message product id 0x02 monitor and control (in switching program?)
# C1 message product id 0x01 monitor only (in listening program)


#TODO change this so it returns a pydict
#write an encoder that turns the pydict into a buffer for the radio

def make_monitor():
    payload = [
        7 + 3 + 3,                  # payload remaining length (header+records+footer)
        0x04,                       # manufacturer id = Energenie
        0x01,                       # product id = 0x01=C1(monitor)  0x02=R1(monitor+control)
        0x01,                       # reserved1 (cryptSeedMSB)
        0x00,                       # reserved2 (cryptSeedLSB)
        # from here up until the NUL is crc'd
        # from here up to and including the CRC is crypted
        0xFF,                       # sensorIdHigh broadcast
        0xFF,                       # sensorIdMid broadcast
        0xFF,                       # sensorIdLow broadcast
        # RECORDS
        PARAM_SWITCH_STATE | 0x80,  # set switch state
        0x01,                       # type/length
        0x00,                       # value off
        0x00                        # NUL
    ]
    # Calculate and append the CRC bytes
    crc = calcCRC(payload, 5, len(payload)-5)
    payload.append((crc >> 8) & 0xFF) # MSB, big-endian
    payload.append(crc & 0xFF)        # LSB

    crypto.init(crypt_pid, crypt_pip)
    crypto.cryptPayload(payload, 5, len(payload)-5) # including CRC
    return payload


#----- CRC CALCULATION --------------------------------------------------------

#int16_t crc(uint8_t const mes[], unsigned char siz)
#{
#	uint16_t rem = 0;
#	unsigned char byte, bit;
#
#	for (byte = 0; byte < siz; ++byte)
#	{
#		rem ^= (mes[byte] << 8);
#		for (bit = 8; bit > 0; --bit)
#		{
#			rem = ((rem & (1 << 15)) ? ((rem << 1) ^ 0x1021) : (rem << 1));
#		}
#	}
#	return rem;
#}

def calcCRC(payload, start, length):
    rem = 0
    for b in payload[start:start+length]:
        rem ^= (b<<8)
        for bit in range(8):
            if rem & (1<<15) != 0:
                # bit is set
                rem = ((rem<<1) ^ 0x1021) & 0xFFFF # always maintain U16
            else:
                # bit is clear
                rem = (rem<<1) & 0xFFFF # always maintain U16
    return rem

# END
