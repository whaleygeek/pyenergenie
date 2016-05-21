# OpenThings_test.py  21/05/2016  D.J.Whale
#
# Test harness for OpenThings protocol encoder and decoder

#TODO: Turn this into unittest.TestCase


from OpenThings import *
import pprint


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