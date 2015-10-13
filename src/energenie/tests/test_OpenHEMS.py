# test_OpenHEMS.py  13/10/2015  E.D.Hurst-Frost
#
# OpenHEMS module tests.
import unittest
from energenie import OpenHEMS


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_Decode_eTRV_temperature_report(self):
        eTRVAnnounce = [0xe,0x4,0x3,0x46,0x13,0x0,0x4,0xae,0x74,0x92,0x14,0xb3,0x0,0xcb,0xc7]
        decoded = OpenHEMS.decode(eTRVAnnounce, False)
        print(decoded)
        self.assertEqual(0x4ae, decoded['header']['sensorid'], "Unexpected sensor ID")
        self.assertEqual('OK', decoded['type'], "Unexpected type")
        self.assertEqual(1, decoded['recs'].__len__(), "Unexpected number of recs")
        self.assertEqual('TEMPERATURE', decoded['recs'][0]['paramname'], "Unexpected number of recs")
        self.assertAlmostEqual(20.7, decoded['recs'][0]['value'], msg="Unexpected value", places=2)

    def test_Decode_MiHome_gateway_ACK(self):
        eTRVACK = [0xa,0x4,0x3,0x2f,0xd2,0x0,0x4,0xae,0x0,0xe2,0xb1]
        decoded = OpenHEMS.decode(eTRVACK, False)
        self.assertEqual(0x4ae, decoded['header']['sensorid'], "Unexpected sensor ID")
        self.assertEqual('OK', decoded['type'], "Unexpected type")
        self.assertEqual(0, decoded['recs'].__len__(), "Unexpected number of recs")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()