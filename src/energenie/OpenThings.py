# OpenThings.py  27/09/2015  D.J.Whale
#
# Implement OpenThings message encoding and decoding

import time
try:
	import crypto # python 2
except ImportError:
	from . import crypto # python 3

class OpenThingsException(Exception):
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
PARAM_RELATIVE_HUMIDITY=0x68
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

param_info = {
	PARAM_ALARM           : {"n":"ALARM",				"u":""},
	PARAM_DEBUG_OUTPUT    : {"n":"DEBUG_OUTPUT",		"u":""},
	PARAM_IDENTIFY        : {"n":"IDENTIFY",			"u":""},
	PARAM_SOURCE_SELECTOR : {"n":"SOURCE_SELECTOR",		"u":""},
	PARAM_WATER_DETECTOR  : {"n":"WATER_DETECTOR",		"u":""},
	PARAM_GLASS_BREAKAGE  : {"n":"GLASS_BREAKAGE",		"u":""},
	PARAM_CLOSURES        : {"n":"CLOSURES",			"u":""},
	PARAM_DOOR_BELL       : {"n":"DOOR_BELL",			"u":""},
	PARAM_ENERGY          : {"n":"ENERGY",				"u":"kWh"},
	PARAM_FALL_SENSOR     : {"n":"FALL_SENSOR",			"u":""},
	PARAM_GAS_VOLUME      : {"n":"GAS_VOLUME",			"u":"m3"},
	PARAM_AIR_PRESSURE    : {"n":"AIR_PRESSURE",		"u":"mbar"},
	PARAM_ILLUMINANCE     : {"n":"ILLUMINANCE",			"u":"Lux"},
	PARAM_LEVEL           : {"n":"LEVEL",				"u":""},
	PARAM_RAINFALL        : {"n":"RAINFALL",			"u":"mm"},
	PARAM_APPARENT_POWER  : {"n":"APPARENT_POWER",		"u":"VA"},
	PARAM_POWER_FACTOR    : {"n":"POWER_FACTOR",		"u":""},
	PARAM_REPORT_PERIOD   : {"n":"REPORT_PERIOD",		"u":"s"},
	PARAM_SMOKE_DETECTOR  : {"n":"SMOKE_DETECTOR",		"u":""},
	PARAM_TIME_AND_DATE   : {"n":"TIME_AND_DATE",		"u":"s"},
	PARAM_VIBRATION       : {"n":"VIBRATION",			"u":""},
	PARAM_WATER_VOLUME    : {"n":"WATER_VOLUME",		"u":"l"},
	PARAM_WIND_SPEED      : {"n":"WIND_SPEED",			"u":"m/s"},
	PARAM_GAS_PRESSURE    : {"n":"GAS_PRESSURE",		"u":"Pa"},
	PARAM_BATTERY_LEVEL   : {"n":"BATTERY_LEVEL",		"u":"V"},
	PARAM_CO_DETECTOR     : {"n":"CO_DETECTOR",			"u":""},
	PARAM_DOOR_SENSOR     : {"n":"DOOR_SENSOR",			"u":""},
	PARAM_EMERGENCY       : {"n":"EMERGENCY",			"u":""},
	PARAM_FREQUENCY       : {"n":"FREQUENCY",			"u":"Hz"},
	PARAM_GAS_FLOW_RATE   : {"n":"GAS_FLOW_RATE",		"u":"m3/hr"},
	PARAM_RELATIVE_HUMIDITY:{"n":"RELATIVE_HUMIDITY",   "u":"%"},
	PARAM_CURRENT         : {"n":"CURRENT",				"u":"A"},
	PARAM_JOIN            : {"n":"JOIN",				"u":""},
	PARAM_LIGHT_LEVEL     : {"n":"LIGHT_LEVEL",			"u":""},
	PARAM_MOTION_DETECTOR : {"n":"MOTION_DETECTOR",		"u":""},
	PARAM_OCCUPANCY       : {"n":"OCCUPANCY",			"u":""},
	PARAM_REAL_POWER      : {"n":"REAL_POWER",			"u":"W"},
	PARAM_REACTIVE_POWER  : {"n":"REACTIVE_POWER",		"u":"VAR"},
	PARAM_ROTATION_SPEED  : {"n":"ROTATION_SPEED",		"u":"RPM"},
	PARAM_SWITCH_STATE    : {"n":"SWITCH_STATE",		"u":""},
	PARAM_TEMPERATURE     : {"n":"TEMPERATURE",			"u":"C"},
	PARAM_VOLTAGE         : {"n":"VOLTAGE",				"u":"V"},
	PARAM_WATER_FLOW_RATE : {"n":"WATER_FLOW_RATE",		"u":"l/hr"},
	PARAM_WATER_PRESSURE  : {"n":"WATER_PRESSURE",		"u":"Pa"},
}


crypt_pid = None

def init(pid):
	global crypt_pid
	crypt_pid = pid


def warning(msg):
	print("warning:" + str(msg))


def trace(msg):
	print("OpenThings:%s" % str(msg))


#----- MESSAGE DECODER --------------------------------------------------------

#TODO if silly lengths or silly types seen in decode, this might imply
#we're trying to process an encrypted packet without decrypting it.
#the code should be more robust to this (by checking the CRC)

def decode(payload, decrypt=True):
	"""Decode a raw buffer into an OpenThings pydict"""
	#Note, decrypt must already have run on this for it to work
	length = payload[0]

	# CHECK LENGTH
	if length+1 != len(payload) or length < 10:
		raise OpenThingsException("bad payload length")
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
		#printhex(payload)
	# sensorId is in encrypted region
	sensorId = (payload[5]<<16) + (payload[6]<<8) + payload[7]
	header["sensorid"] = sensorId


	# CHECK CRC
	crc_actual  = (payload[-2]<<8) + payload[-1]
	crc_expected = calcCRC(payload, 5, len(payload)-(5+2))
	#trace("crc actual:%s, expected:%s" %(hex(crc_actual), hex(crc_expected)))

	if crc_actual != crc_expected:
		raise OpenThingsException("bad CRC")
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
		if paramid in param_info:
			paramname = (param_info[paramid])["n"] # name
			paramunit = (param_info[paramid])["u"] # unit
		else:
			paramname = "UNKNOWN_" + hex(paramid)
			paramunit = "UNKNOWN_UNIT"
		i += 1

		# TYPE/LEN
		typeid = payload[i] & 0xF0
		plen = payload[i] & 0x0F
		i += 1

		rec = {
			"wr":         wr,
			"paramid":    paramid,
			"paramname":  paramname,
			"paramunit":  paramunit,
			"typeid":     typeid,
			"length":     plen
		}

		if plen != 0:
			# VALUE
			valuebytes = []
			for x in range(plen):
				valuebytes.append(payload[i])
				i += 1
			value = Value.decode(valuebytes, typeid, plen)
			rec["valuebytes"] = valuebytes
			rec["value"] = value

		# store rec
		recs.append(rec)

	return {
		"type":    "OK",
		"header":  header,
		"recs":    recs
	}


#----- MESSAGE ENCODER --------------------------------------------------------
#
# Encodes a message using the OpenThings message payload structure

# R1 message product id 0x02 monitor and control (in switching program?)
# C1 message product id 0x01 monitor only (in listening program)

def encode(spec, encrypt=True):
	"""Encode a pydict specification into a OpenThings binary payload"""
	# The message is not encrypted, but the CRC is generated here.

	payload = []

	# HEADER
	payload.append(0) # length, fixup later when known
	header = spec["header"]

	payload.append(header["mfrid"])
	payload.append(header["productid"])

	if not ("encryptPIP" in header):
		if encrypt:
			warning("no encryptPIP in header, assuming 0x0100")
		encryptPIP = 0x0100
	else:
		encryptPIP = header["encryptPIP"]
	payload.append((encryptPIP&0xFF00)>>8) # MSB
	payload.append((encryptPIP&0xFF))      # LSB

	sensorId = header["sensorid"]
	payload.append((sensorId>>16) & 0xFF) # HIGH
	payload.append((sensorId>>8) & 0xFF)  # MID
	payload.append((sensorId) & 0XFF)     # LOW

	# RECORDS
	for rec in spec["recs"]:
		wr      = rec["wr"]
		paramid = rec["paramid"]
		typeid  = rec["typeid"]
		if "length" in rec:
			length  = rec["length"]
		else:
			length = None # auto detect

		# PARAMID
		if wr:
			payload.append(0x80 + paramid) # WRITE
		else:
			payload.append(paramid)        # READ

		# TYPE/LENGTH
		payload.append((typeid)) # need to back patch length for auto detect
		lenpos = len(payload)-1 # for backpatch

		# VALUE
		valueenc = [] # in case of no value
		if "value" in rec:
			value = rec["value"]
			valueenc = Value.encode(value, typeid, length)
			if len(valueenc) > 15:
				raise ValueError("value longer than 15 bytes")
			for b in valueenc:
				payload.append(b)
			payload[lenpos] = (typeid) | len(valueenc)

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


#---- VALUE CODEC -------------------------------------------------------------

class Value():
	UINT      = 0x00
	UINT_BP4  = 0x10
	UINT_BP8  = 0x20
	UINT_BP12 = 0x30
	UINT_BP16 = 0x40
	UINT_BP20 = 0x50
	UINT_BP24 = 0x60
	CHAR      = 0x70
	SINT      = 0x80
	SINT_BP8  = 0x90
	SINT_BP16 = 0xA0
	SINT_BP24 = 0xB0
	# C0,D0,E0 RESERVED
	FLOAT     = 0xF0

	@staticmethod
	def typebits(typeid):
		"""work out number of bits to represent this type"""
		if typeid == Value.UINT_BP4:  return 4
		if typeid == Value.UINT_BP8:  return 8
		if typeid == Value.UINT_BP12: return 12
		if typeid == Value.UINT_BP16: return 16
		if typeid == Value.UINT_BP20: return 20
		if typeid == Value.UINT_BP24: return 24
		if typeid == Value.SINT_BP8:  return 8
		if typeid == Value.SINT_BP16: return 16
		if typeid == Value.SINT_BP24: return 24
		raise ValueError("Can't calculate number of bits for type:" + str(typeid))


	@staticmethod
	def highestClearBit(value, maxbits=15*8):
		"""Find the highest clear bit scanning MSB to LSB"""
		mask = 1<<(maxbits-1)
		bitno = maxbits-1
		while mask != 0:
			#trace("compare %s with %s" %(hex(value), hex(mask)))
			if (value & mask) == 0:
				#trace("zero at bit %d" % bitno)
				return bitno
			mask >>= 1
			bitno-=1
		#trace("not found")
		return None # NOT FOUND


	@staticmethod
	def valuebits(value):
		"""Work out number of bits required to represent this value"""
		if value >= 0 or type(value) != int:
			raise RuntimeError("valuebits only on -ve int at moment")

		if value == -1: # always 0xFF, so always needs exactly 2 bits to represent (sign and value)
			return 2 # bits required
		#trace("valuebits of:%d" % value)
		# Turn into a 2's complement representation
		MAXBYTES=15
		MAXBITS = 1<<(MAXBYTES*8)
		#TODO check for truncation?
		value = value & MAXBITS-1
		#trace("hex:%s" % hex(value))
		highz = Value.highestClearBit(value, MAXBYTES*8)
		#trace("highz at bit:%d" % highz)
		# allow for a sign bit, and bit numbering from zero
		neededbits = highz+2

		#trace("needed bits:%d" % neededbits)
		return neededbits


	@staticmethod
	def encode(value, typeid, length=None):
		#trace("encoding:" + str(value))
		if typeid == Value.CHAR:
			if type(value) != str:
				value = str(value)
			if length != None and len(str) > length:
				raise ValueError("String too long")
			result = []
			for ch in value:
				result.append(ord(ch))
			if len != None and len(result) < length:
				for a in range(length-len(result)):
					result.append(0) # zero pad
			return result

		if typeid == Value.FLOAT:
			raise ValueError("IEEE-FLOAT not yet supported")

		if typeid <= Value.UINT_BP24:
			# unsigned integer
			if value < 0:
				raise ValueError("Cannot encode negative number as an unsigned int")

			if typeid != Value.UINT:
				# pre-adjust for BP
				if type(value) == float:
					value *= (2**Value.typebits(typeid)) # shifts float into int range using BP
					value = round(value, 0) # take off any unstorable bits
			value = int(value) # It must be an integer for the next part of encoding

			# code it in the minimum length bytes required
			# Note that this codes zero in 0 bytes (might not be correct?)
			v = value
			result = []
			while v != 0:
				result.insert(0, v&0xFF) # MSB first, so reverse bytes as inserting
				v >>= 8

			# check length mismatch and zero left pad if required
			if length != None:
				if len(result) < length:
					result = [0 for x in range(length-len(result))] + result
				elif len(result) > length:
					raise ValueError("Field width overflow, not enough bits")
			return result


		if typeid >= Value.SINT and typeid <= Value.SINT_BP24:
			# signed int
			if typeid != Value.SINT:
				# pre-adjust for BP
				if type(value) == float:
					value *= (2**Value.typebits(typeid)) # shifts float into int range using BP
					value = round(value, 0) # take off any unstorable bits
			value = int(value) # It must be an integer for the next part of encoding

			#If negative, take complement by masking with the length mask
			# This turns -1 (8bit) into 0xFF, which is correct
			# -1 (16bit) into 0xFFFF, which is correct
			# -128(8bit) into 0x80, which is correct
			#i.e. top bit will always be set as will all following bits up to number

			if value < 0: # -ve
				if typeid == Value.SINT:
					bits = Value.valuebits(value)
				else:
					bits = Value.typebits(typeid)
				#trace("need bits:" + str(bits))
				# NORMALISE BITS TO BYTES
				####HERE#### round up to nearest number of 8 bits
				# if already 8, leave 1,2,3,4,5,6,7,8 = 8   0,1,2,3,4,5,6,7 (((b-1)/8)+1)*8
				# 9,10,11,12,13,14,15,16=16
				bits = (((bits-1)/8)+1)*8 # snap to nearest byte boundary
				#trace("snap bits to 8:" + str(bits))

				value &= ((2**bits)-1)
				neg = True
			else:
				neg = False

			#encode in minimum bytes possible
			v = value
			result = []
			while v != 0:
				result.insert(0, v&0xFF) # MSB first, so reverse when inserting
				v >>= 8

			# if desired length mismatch, zero pad or sign extend to fit
			if length != None: # fixed size
				if len(result) < length: # pad
					if not neg:
						result = [0 for x in range(length-len(result))] + result
					else: # negative
						result = [0xFF for x in range(length-len(result))] + result
				elif len(result) >length: # overflow
					raise ValueError("Field width overflow, not enough bits")

			return result

		raise ValueError("Unknown typeid:%d" % typeid)


	@staticmethod
	def decode(valuebytes, typeid, length):
		if typeid <= Value.UINT_BP24:
			result = 0
			# decode unsigned integer first
			for i in range(length):
				result <<= 8
				result += valuebytes[i]
			# process any fixed binary points
			if typeid == Value.UINT:
				return result # no BP adjustment
			return (float(result)) / (2**Value.typebits(typeid))

		elif typeid == Value.CHAR:
			result = ""
			for b in range(length):
				result += chr(b)
			return result

		elif typeid >= Value.SINT and typeid <= Value.SINT_BP24:
			# decode unsigned int first
			result = 0
			for i in range(length):
				result <<= 8
				result += valuebytes[i]

			# turn to signed int based on high bit of MSB
			# 2's comp is 1's comp plus 1
			neg = ((valuebytes[0] & 0x80) == 0x80)
			if neg:
				onescomp = (~result) & ((2**(length*8))-1)
				result = -(onescomp + 1)

			# adjust for binary point
			if typeid == Value.SINT:
				return result # no BP, return as int
			else:
				# There is a BP, return as float
				return (float(result))/(2**Value.typebits(typeid))

		elif typeid == Value.FLOAT:
			return "TODO_FLOAT_IEEE_754-2008" #TODO: IEEE 754-2008

		raise ValueError("Unsupported typeid:%" + hex(typeid))


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


def showMessage(msg, timestamp=None):
	"""Show the message in a friendly format"""

	# HEADER
	header    = msg["header"]
	mfrid     = header["mfrid"]
	productid = header["productid"]
	sensorid  = header["sensorid"]
	if timestamp != None:
		print("receive-time:%s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
	print("mfrid:%s prodid:%s sensorid:%s" % (hex(mfrid), hex(productid), hex(sensorid)))

	# RECORDS
	for rec in msg["recs"]:
		wr = rec["wr"]
		if wr == True:
			write = "write"
		else:
			write = "read "

		paramid   = rec["paramid"]
		paramname = rec["paramname"]
		paramunit = rec["paramunit"]
		if "value" in rec:
				value = rec["value"]
		else:
				value = None
		print("%s %s %s = %s" % (write, paramname, paramunit, str(value)))


def alterMessage(message, **kwargs):
	"""Change parameters in-place in a message template"""
	# e.g. header_sensorid=1234, recs_0_value=1
	for arg in kwargs:

		path = arg.split("_")
		value = kwargs[arg]

		m = message
		for p in path[:-1]:
			try:
				p = int(p)
			except:
				pass
			m = m[p]
		#trace("old value:%s" % m[path[-1]])
		m[path[-1]] = value

		#trace("modified:" + str(message))

	return message


def getFromMessage(message, keypath):
	"""Get a field from a message, given an underscored keypath to the item"""
	path = keypath.split("_")

	for p in path[:-1]:
		try:
			p = int(p)
		except:
			pass
		message = message[p]
	return message[path[-1]]


#----- TEST HARNESS -----------------------------------------------------------

def printhex(payload):
	line = ""
	for b in payload:
		line += hex(b) + " "

	print(line)


TEST_PAYLOAD = [
	0x1C, 						#len   16 + 10 + 2  = 0001 1100
	0x04, 						#mfrid
	0x02, 						#prodid
	0x01, 						#pipmsb
	0x00, 						#piplsb
	0x00, 0x06, 0x8B,        	#sensorid
	0x70, 0x82, 0x00, 0x07, 	#SINT(2)     power
	0x71, 0x82, 0xFF, 0xFD,     #SINT(2)     reactive_power
	0x76, 0x01, 0xF0,    		#UINT(1)     voltage
	0x66, 0x22, 0x31, 0xDA,		#UINT_BP8(2) freq
	0x73, 0x01, 0x01,			#UINT(1)     switch_state
	0x00,						#NUL
	0x97, 0x64					#CRC

]

import pprint


def test_payload_unencrypted():
	init(242)

	printhex(TEST_PAYLOAD)
	spec = decode(TEST_PAYLOAD, decrypt=False)
	pprint.pprint(spec)

	payload = encode(spec, encrypt=False)
	printhex(payload)

	spec2 = decode(payload, decrypt=False)
	pprint.pprint(spec2)

	payload2 = encode(spec2, encrypt=False)

	printhex(TEST_PAYLOAD)
	printhex(payload2)

	if TEST_PAYLOAD != payload:
		print("FAILED")
	else:
		print("PASSED")


def test_payload_encrypted():
	init(242)

	printhex(TEST_PAYLOAD)
	spec = decode(TEST_PAYLOAD, decrypt=False)
	pprint.pprint(spec)

	payload = encode(spec, encrypt=True)
	printhex(payload)

	spec2 = decode(payload, decrypt=True)
	pprint.pprint(spec2)

	payload2 = encode(spec2, encrypt=False)

	printhex(TEST_PAYLOAD)
	printhex(payload2)

	if TEST_PAYLOAD != payload:
		print("FAILED")
	else:
		print("PASSED")


def test_value_encoder():
	pass
	# test cases (auto, forced, overflow, -min, -min-1, 0, 1, +max, +max+1
	# UINT
	# UINT_BP4
	# UINT_BP8
	# UINT_BP12
	# UINT_BP16
	# UINT_BP20
	# UINT_BP24
	# SINT
	# SINT(2)
	vin = [1,255,256,32767,32768,0,-1,-2,-3,-127,-128,-129,-32767,-32768]
	for v in vin:
		vout = Value.encode(v, Value.SINT)
		print("encode " + str(v) + " " + str(vout))
	# SINT_BP8
	# SINT_BP16
	# SINT_BP24
	# CHAR
	# FLOAT


def test_value_decoder():
	pass
	# test cases (auto, forced, overflow, -min, -min-1, 0, 1, +max, +max+1
	# UINT
	# UINT_BP4
	# UINT_BP8
	# UINT_BP12
	# UINT_BP16
	# UINT_BP20
	# UINT_BP24
	# SINT
	vin = [255, 253]
	print("input value:" + str(vin))
	vout = Value.decode(vin, Value.SINT, 2)
	print("encoded as:" + str(vout))

	# SINT_BP8
	# SINT_BP16
	# SINT_BP24
	# CHAR
	# FLOAT


if __name__ == "__main__":
	#test_value_encoder()
	#test_value_decoder()
	test_payload_unencrypted()
	#test_payload_encrypted()

# END
