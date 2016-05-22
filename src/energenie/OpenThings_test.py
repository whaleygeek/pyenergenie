# OpenThings_test.py  21/05/2016  D.J.Whale
#
# Test harness for OpenThings protocol encoder and decoder

#TODO: Turn this into unittest.TestCase


from OpenThings import *
import pprint
import unittest


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


#----- UNIT TEST FOR MESSAGE --------------------------------------------------

import Devices

# ACCESSOR VARIANTS
#  as method parameters:
#     {pydict}
#
#     header={pydict}
#     header_mfrid=123
#
#     recs_0={pydict}
#     recs_0_paramid=PARAM_SWITCH_STATE
#     recs_SWITCH_STATE={pydict}
#     recs_SWITCH_STATE_value=1
#
#  as attribute accessors
#    msg["header"]
#    msg["recs"][0]
#    msg[PARAM_SWITCH_STATE]


class TestMessage(unittest.TestCase):

	def test_blank(self):
		# create a blank message
		msg = Message()
		msg.dump()

	def test_blank_create_dict(self):
		msg = Message({"header":{}, "recs":[{"parmid":PARAM_SWITCH_STATE, "value":1}]})
		msg.dump()

	#### HEADER

	def XXXtest_blank_create_header_dict(self):
		# create a blank message and add a header at creation from a dict
		msg = Message(header={"mfrid":123, "productid":456, "sensorid":789})
		msg.dump()

	def XXXtest_blank_create_header_paths(self):
		# create a blank message and add some header fields at creation time
		msg = Message(header_mfrid=123, header_productid=456, header_sensorid=789)
		msg.dump()

	def XXXtest_add_header_attr(self):
		# add header fields to a message after creation like a pydict
		msg = Message()
		msg["header"]["mfrid"] = 123
		msg.dump()

	def XXXtest_add_header_path(self):
		# add header fields to a message after creation via pathed keys
		msg = Message()
		msg.add(header_mfrid=123, header_productid=456)
		msg.dump()

	def XXXtest_add_header_dict(self):
		msg = Message()
		msg.add(header={"mfrid":123, "productid":456, "sensorid":789})
		msg.dump()

	#### RECORDS

	def XXXtest_add_rec_attr(self):
		# add rec fields to a message after creation like a pydict
		msg = Message()
		msg["recs"][0] = {"paramid": PARAM_SWITCH_STATE, "value": 1}
		msg.dump()

	def XXXtest_add_rec_path(self):
		# add rec fields to a message after creation via pathed indexed keys
		msg = Message()
		msg.add(recs_0_paramid=PARAM_SWITCH_STATE, recs_0_value=1)
		msg.dump()

	def XXXtest_add_rec_fn(self):
		# add rec fields to a message after creation via pathed PARAM name keys
		msg = Message()
		msg.add_rec(PARAM_SWITCH_STATE, value=1)
		msg.dump()

	def XXXtest_add_rec_dict(self):
		# add rec fields from a dict parameter
		msg = Message()
		msg.add_rec({"paramid":PARAM_SWITCH_STATE, "value":1})

	def XXXtest_create_template(self):
		# create a message from a template
		msg = Message(Devices.MIHO005_REPORT)
		msg.dump()

	def XXXtest_alter_rec_template(self):
		# alter rec fields in a template
		msg = Message(Devices.MIHO005_REPORT)
		msg.alter(header_productid=123)
		msg.dump()

	def XXXtest_alter_rec_template_paramname(self):
		# alter rec fields in a template
		msg = Message(Devices.MIHO005_REPORT)
		msg.alter(recs_SWITCH_STATE_value=1)
		msg.dump()

	def XXXtest_pydict_read(self):
		## access a specific keyed entry like a normal pydict, for read
		msg = Message(Devices.MIHO005_REPORT)
		print(msg["header"])
		print(msg["header"]["mfrid"])

	def XXXtest_pydict_write(self):
		## access a specific keyed entry like a normal pydict, for write
		msg = Message(Devices.MIHO005_REPORT)
		msg["header"]["mfrid"] = 222
		msg.dump()

	def XXXtest_paramid_read_struct(self):
		# access a paramid entry for read of the whole structure
		msg = Message(Devices.MIHO005_REPORT)
		print(msg[PARAM_SWITCH_STATE])

	def XXXtest_paramid_read_field(self):
		## read a value from a param id field that exists
		msg = Message(Devices.MIHO005_REPORT)
		print(msg[PARAM_SWITCH_STATE]["value"])

	def XXXtest_paramid_write(self):
		## write a value to a param id field that exists
		msg = Message(Devices.MIHO005_REPORT)
		msg[PARAM_SWITCH_STATE]["value"] = 1
		msg.dump()


	def XXXtest_repr(self):
		## dump a message in printable format
		msg = Message(Devices.MIHO005_REPORT)
		print(msg)

	def XXXtest_str(self):
		## dump a message in printable format
		msg = Message(Devices.MIHO005_REPORT)
		print(str(msg))


def test_message():
	import unittest
	unittest.main()

if __name__ == "__main__":
	##TODO: Change these into unittest test cases
	##test_value_encoder()
	##test_value_decoder()
	##test_payload_unencrypted()
	##test_payload_encrypted()

	test_message()

# END