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
#     1  {pydict}
#
#     2  header={pydict}
#     3  header_mfrid=123
#     4  recs_0={pydict}
#     5  recs_0_paramid=PARAM_SWITCH_STATE
#     6  SWITCH_STATE={pydict}
#     7  SWITCH_STATE,value=1
#     8  SWITCH_STATE_value=1
#
#  as attribute accessors
#     9  msg["header"]  msg["recs"][0]
#     10 msg[PARAM_SWITCH_STATE]


class TestMessage(unittest.TestCase):

	def XXXtest_blank(self):
		"""CREATE a completely blank message"""
		msg = Message()
		print(msg.pydict)
		msg.dump()

	def XXXtest_blank_template(self):
		"""CREATE a message from a simple pydict template"""
		# This is useful to simplify all other tests
		msg = Message(Message.BLANK)
		print(msg.pydict)
		msg.dump()

	def XXXtest_blank_create_dict(self): #1 {pydict}
		"""CREATE a blank message with a dict parameter"""
		msg = Message({"header":{}, "recs":[{"wr":False, "parmid":PARAM_SWITCH_STATE, "value":1}]})
		print(msg.pydict)
		msg.dump()

	def XXXtest_blank_create_header_dict(self): #2 header={pydict}
		"""CREATE a blank message and add a header at creation time from a dict"""
		msg = Message(header={"mfrid":123, "productid":456, "sensorid":789})
		print(msg.pydict)
		msg.dump()

	def XXXtest_create_big_template(self): #1 {pydict}
		"""CREATE from a large template message"""
		# create a message from a template
		msg = Message(Devices.MIHO005_REPORT)
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_rec_dict(self): #1 {pydict}
		"""UPDATE(APPEND) rec fields from a dict parameter"""
		msg = Message(Message.BLANK)
		i = msg.append_rec({"paramid":PARAM_SWITCH_STATE, "wr":True, "value":1})
		print("added index:%d" % i)
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_header_dict(self): #2 header={pydict}
		"""UPDATE(SET) a new header to an existing message"""
		msg = Message()
		msg.set(header={"mfrid":123, "productid":456, "sensorid":789})
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_recs_dict(self):
		"""UPDATE(SET) recs to an existing message"""
		msg = Message()
		msg.set(recs=[{"paramid":PARAM_SWITCH_STATE, "wr":True, "value":1}])
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_path(self):
		"""UPDATE(SET) a pathed key to an existing message"""
		msg = Message()
		msg.set(header_productid=1234)
		print(msg.pydict)
		msg.dump()

	def XXXtest_alter_template(self): #3 header_mfrid=123
		"""UPDATE(SET) an existing key with a path"""
		msg = Message(Devices.MIHO005_REPORT)
		msg.set(header_productid=123)
		msg.dump()

	def XXXtest_alter_template_multiple(self):
		"""UPDATE(SET) multiple keys with paths"""
		msg = Message(Devices.MIHO005_REPORT)
		msg.set(header_productid=123, header_sensorid=99)
		print(msg.pydict)
		msg.dump()

	def XXXtest_blank_create_header_paths(self): #3 header_mfrid=123    (CREATE)
		"""CREATE message with pathed keys in constructor"""
		msg = Message(header_mfrid=123, header_productid=456, header_sensorid=789)
		print(msg.pydict)
		msg.dump()

	def XXXtest_blank_create_recs_paths(self):
		"""CREATE message with pathed keys in constructor"""
		# uses integer path component to mean array index
		msg = Message(recs_0={"paramid":PARAM_SWITCH_STATE, "wr":True, "value":1},
					  recs_1={"paramid":PARAM_AIR_PRESSURE, "wr":True, "value":2})
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_rec_path(self): #5 recs_0_paramid=PARAM_SWITCH_STATE
		"""UPDATE(SET) records in a message"""
		msg = Message(recs_0={}) # must create rec before you can change it
		print(msg.pydict)
		msg.set(recs_0_paramid=PARAM_SWITCH_STATE, recs_0_value=1, recs_0_wr=True)
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_rec_fn_pydict(self): #6 SWITCH_STATE={pydict}
		"""UPDATE(ADD) a rec to message using PARAM constants as keys"""
		#always creates a new rec at the end and then populates
		msg = Message()
		msg.append_rec(PARAM_SWITCH_STATE, {"wr": True, "value":1})
		print(msg.pydict)
		msg.dump()

	def XXXtest_add_rec_fn_keyed(self): #7 SWITCH_STATE,value=1    (ADD)
		"""UPDATE(ADD) a rec to message using PARAM const and keyed values"""
		msg = Message()
		msg.append_rec(PARAM_SWITCH_STATE, wr=True, value=1)
		print(msg.pydict)
		msg.dump()

	def XXXtest_get_pathed(self):
		"""READ from the message with a path key"""
		msg = Message(Devices.MIHO005_REPORT)
		print(msg.get("header_mfrid"))

	#----- HERE -----

	#### This is the attribute set/get abstraction

	def XXXtest_pydict_read(self): #9 msg["header"]  msg["recs"][0]    (READ)
		## access a specific keyed entry like a normal pydict, for read
		msg = Message(Devices.MIHO005_REPORT)
		print(msg["header"])
		print(msg["header"]["mfrid"])

	def XXXtest_pydict_write(self): #9 msg["header"]  msg["recs"][0]    (CHANGE)
		## access a specific keyed entry like a normal pydict, for write
		msg = Message(Devices.MIHO005_REPORT)
		msg["header"]["mfrid"] = 222
		msg.dump()

	def XXXtest_add_header_attr(self): #9 msg["header"]  msg["recs"][0]    (CHANGE)
		# add header fields to a message after creation like a pydict
		msg = Message()
		msg["header"]["mfrid"] = 123
		msg.dump()

	def XXXtest_add_rec_attr(self): #9 msg["header"]  msg["recs"][0]    (CHANGE)
		# add rec fields to a message after creation like a pydict
		msg = Message()
		msg["recs"][0] = {"paramid": PARAM_SWITCH_STATE, "value": 1}
		msg.dump()


	#### This is the PARAMID indexer

	def XXXtest_paramid_read_struct(self): #10 msg[PARAM_SWITCH_STATE]    (READ)
		# access a paramid entry for read of the whole structure
		msg = Message(Devices.MIHO005_REPORT)
		print(msg[PARAM_SWITCH_STATE])

	def XXXtest_paramid_read_field(self): #10 msg[PARAM_SWITCH_STATE]    (READ)
		## read a value from a param id field that exists
		msg = Message(Devices.MIHO005_REPORT)
		print(msg[PARAM_SWITCH_STATE]["value"])

	def XXXtest_paramid_write(self): #10 msg[PARAM_SWITCH_STATE]    (CHANGE)
		## write a value to a param id field that exists
		msg = Message(Devices.MIHO005_REPORT)
		msg[PARAM_SWITCH_STATE]["value"] = 1
		msg.dump()



	####TODO: This is where we need an intelligent key parser

	def XXXtest_alter_rec_template_paramname(self): #8 SWITCH_STATE_value=1    (CHANGE)
		# alter rec fields in a template
		msg = Message(Devices.MIHO005_REPORT)
		msg.set(recs_SWITCH_STATE_value=1)
		msg.dump()


	####TODO: This is where dump() might need to dump to a strbuf and then output
	#some of these might just print the inner pydict though
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