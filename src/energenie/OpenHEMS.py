# OpenHEMS.py  27/09/2015  D.J.Whale
#
# Implement OpenHEMS message encoding and decoding

import crypto

class OpenHEMSException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


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

param_names = {
	PARAM_ALARM           : "ALARM",
	PARAM_DEBUG_OUTPUT    : "DEBUG_OUTPUT",
	PARAM_IDENTIFY        : "IDENTIFY",
	PARAM_SOURCE_SELECTOR : "SOURCE_SELECTOR",
	PARAM_WATER_DETECTOR  : "WATER_DETECTOR",
	PARAM_GLASS_BREAKAGE  : "GLASS_BREAKAGE",
	PARAM_CLOSURES        : "CLOSURES",
	PARAM_DOOR_BELL       : "DOOR_BELL",
	PARAM_ENERGY          : "ENERGY",
	PARAM_FALL_SENSOR     : "FALL_SENSOR",
	PARAM_GAS_VOLUME      : "GAS_VOLUME",
	PARAM_AIR_PRESSURE    : "AIR_PRESSURE",
	PARAM_ILLUMINANCE     : "ILLUMINANCE",
	PARAM_LEVEL           : "LEVEL",
	PARAM_RAINFALL        : "RAINFALL",
	PARAM_APPARENT_POWER  : "APPARENT_POWER",
	PARAM_POWER_FACTOR    : "POWER_FACTOR",
	PARAM_REPORT_PERIOD   : "REPORT_PERIOD",
	PARAM_SMOKE_DETECTOR  : "SMOKE_DETECTOR",
	PARAM_TIME_AND_DATE   : "TIME_AND_DATE",
	PARAM_VIBRATION       : "VIBRATION",
	PARAM_WATER_VOLUME    : "WATER_VOLUME",
	PARAM_WIND_SPEED      : "WIND_SPEED",
	PARAM_GAS_PRESSURE    : "GAS_PRESSURE",
	PARAM_BATTERY_LEVEL   : "BATTERY_LEVEL",
	PARAM_CO_DETECTOR     : "CO_DETECTOR",
	PARAM_DOOR_SENSOR     : "DOOR_SENSOR",
	PARAM_EMERGENCY       : "EMERGENCY",
	PARAM_FREQUENCY       : "FREQUENCY",
	PARAM_GAS_FLOW_RATE   : "GAS_FLOW_RATE",
	PARAM_CURRENT         : "CURRENT",
	PARAM_JOIN            : "JOIN",
	PARAM_LIGHT_LEVEL     : "LIGHT_LEVEL",
	PARAM_MOTION_DETECTOR : "MOTION_DETECTOR",
	PARAM_OCCUPANCY       : "OCCUPANCY",
	PARAM_REAL_POWER      : "REAL_POWER",
	PARAM_REACTIVE_POWER  : "REACTIVE_POWER",
	PARAM_ROTATION_SPEED  : "ROTATION_SPEED",
	PARAM_SWITCH_STATE    : "SWITCH_STATE",
	PARAM_TEMPERATURE     : "TEMPERATURE",
	PARAM_VOLTAGE         : "VOLTAGE",
	PARAM_WATER_FLOW_RATE : "WATER_FLOW_RATE",
	PARAM_WATER_PRESSURE  : "WATER_PRESSURE"
}


crypt_pid = None

def init(pid):
	global crypt_pid
	crypt_pid = pid


def warning(msg):
	print("warning:" + str(msg))


#----- MESSAGE DECODER --------------------------------------------------------

#TODO if silly lengths or silly types seen in decode, this might imply
#we're trying to process an encrypted packet without decrypting it.
#the code should be more robust to this (by checking the CRC)

def decode(payload, decrypt=True):
	"""Decode a raw buffer into an OpenHEMS pydict"""
	#Note, decrypt must already have run on this for it to work
	length = payload[0]

	# CHECK LENGTH
	if length+1 != len(payload) or length < 10:
		raise OpenHEMSException("bad payload length")
		#return {
		#	"type":         "BADLEN",
		#	"len_actual":   len(payload),
		#	"len_expected": length,
		#	"payload":      payload[1:]
		#}

	# DECODE HEADER
	mfrId      = payload[1]
	productId  = payload[2]
	encryptPIP = (payload[3]<<8) + payload[4]
	header = {
		"mfrid"     : mfrId,
		"productid" : productId,
		"encryptPIP": encryptPIP
	}


	if decrypt:
		# DECRYPT PAYLOAD
		# [0]len,mfrid,productid,pipH,pipL,[5]
		crypto.init(crypt_pid, encryptPIP)
		crypto.cryptPayload(payload, 5, len(payload)-5) # including CRC

	# sensorId is in encrypted region
	sensorId = (payload[5]<<16) + (payload[6]<<8) + payload[7]
	header["sensorid"] = sensorId


	# CHECK CRC
	crc_actual  = (payload[-2]<<8) + payload[-1]
	crc_expected = calcCRC(payload, 5, len(payload)-(5+2))
	#print("crc actual:%s, expected:%s" %(hex(crc_actual), hex(crc_expected)))

	if crc_actual != crc_expected:
		raise OpenHEMSException("bad CRC")
		#return {
		#	"type":         "BADCRC",
		#	"crc_actual":   crc_actual,
		#	"crc_expected": crc_expected,
		#	"payload":      payload[1:],
		#}


	# DECODE RECORDS
	i = 8
	recs = []
	while i < length and payload[i] != 0:
		# PARAM
		param = payload[i]
		wr = ((param & 0x80) == 0x80)
		paramid = param & 0x7F
		if param_names.has_key(paramid):
			paramname = param_names[paramid]
		else:
			paramname = "UNKNOWN_" + hex(paramid)
		i += 1

		# TYPE/LEN
		typeid = (payload[i] & 0xF0)>>4
		plen = payload[i] & 0x0F
		i += 1

		if plen == 0: continue # no more data in this record

		# VALUE
		valuebytes = []
		for x in range(plen):
			valuebytes.append(payload[i])
			i += 1
		value = "TODO" # TODO decode based on type and length

		# store rec
		recs.append({
			"wr":         wr,
			"paramid":    paramid,
			"paramname":  paramname,
			"typeid":     typeid,
			"length":     plen,
			"valuebytes": valuebytes,
			"value":      value
		})

	return {
		"type":    "OK",
		"header":  header,
		"recs":    recs
	}



#----- MESSAGE ENCODER --------------------------------------------------------
#
# Encodes a message using the OpenHEMS message payload structure

# R1 message product id 0x02 monitor and control (in switching program?)
# C1 message product id 0x01 monitor only (in listening program)

def encode(spec, encrypt=True):
	"""Encode a pydict specification into a OpenHEMS binary payload"""
	# The message is not encrypted, but the CRC is generated here.

	payload = []

	# HEADER
	payload.append(0) # length, fixup later when known
	header = spec["header"]

	payload.append(header["mfrid"])
	payload.append(header["productid"])

	if encrypt:
		if not header.has_key("encryptPIP"):
			warning("no encryptPIP in header, assuming 0x0100")
			encryptPIP = 0x0100
		else:
			encryptPIP = header["encryptPIP"]
		payload.append((encryptPIP&0xFF00)>>8) # MSB
		payload.append((encryptPIP&0xFF))      # LSB
	else:
		payload.append(0)
		payload.append(0)

	sensorId = header["sensorid"]
	payload.append((sensorId>>16) & 0xFF) # HIGH
	payload.append((sensorId>>8) & 0xFF)  # MID
	payload.append((sensorId) & 0XFF)     # LOW

	# RECORDS
	for rec in spec["recs"]:
		wr      = rec["wr"]
		paramid = rec["paramid"]
		typeid  = rec["typeid"]
		length  = rec["length"]
		value   = rec["value"]

		# PARAMID
		if wr:
			payload.append(0x80 + paramid) # WRITE
		else:
			payload.append(paramid)        # READ

		# TYPE/LENGTH
		payload.append((typeid<<4) | length)

		# VALUE
		for i in range(length):
			payload.append(0) # TODO encoding depends on typeid and length

	# FOOTER
	payload.append(0) # NUL
	crc = calcCRC(payload, 5, len(payload)-5)
	payload.append((crc>>8) & 0xFF) # MSB
	payload.append(crc&0xFF)        # LSB

	# back-patch the length byte so it is correct
	payload[0] = len(payload)-1

	if encrypt:
		# ENCRYPT
		# [0]len,mfrid,productid,pipH,pipL,[5]
		crypto.init(crypt_pid, encryptPIP)
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


#----- TEST HARNESS -----------------------------------------------------------

def printhex(payload):
	line = ""
	for b in payload:
		line += hex(b) + " "

	print line


if __name__ == "__main__":
	TEST_PAYLOAD = [
		0x1C, 						#len   16 + 10 + 2  = 0001 1100
		0x04, 						#mfrid
		0x02, 						#prodid
		0x01, 						#pipmsb
		0x00, 						#piplsb
		0x00, 0x06, 0x8B,        	#sensorid
		0x70, 0x82, 0x00, 0x07, 	#power
		0x71, 0x82, 0xFF, 0xFD,     #reactive_power
		0x76, 0x01, 0xF0,    		#voltage
		0x66, 0x22, 0x31, 0xDA,		#freq
		0x73, 0x01, 0x01,			#switch_state
		0x00,						#NUL
		0x97, 0x64					#CRC

	]

	import pprint
	init(242)

	printhex(TEST_PAYLOAD)

	spec = decode(TEST_PAYLOAD, decrypt=False)
	pprint.pprint(spec)

	payload = encode(spec, encrypt=True)
	printhex(payload)

	spec2 = decode(payload, decrypt=True)
	pprint.pprint(spec2)

# END
