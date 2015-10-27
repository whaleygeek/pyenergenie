# test_messages.py  13/10/2015  E.D.Hurst-Frost
#
# Devices messages tests.
import unittest
from energenie import OpenHEMS
from messages import MESSAGE_ETRV_SEND_BATTERY_LEVEL

class Test(unittest.TestCase):


    def test_alterMessage(self):
        message = OpenHEMS.encode(OpenHEMS.alterMessage(MESSAGE_ETRV_SEND_BATTERY_LEVEL, header_sensorid=0x1234), False)
        self.assertEqual([0xc,0x4,0x3,0x1,0x0,0x0,0x12,0x34,0x76,0x0,0x0,0xcc,0x69], message);


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()