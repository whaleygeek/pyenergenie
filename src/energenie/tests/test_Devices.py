# test_Devices.py  13/10/2015  E.D.Hurst-Frost
#
# Devices module tests.
import unittest
from energenie import Devices

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        self.assertEqual("Manufactuer:Energenie Product:C1 MONITOR", Devices.getDescription(0x04,0x01), "")
        self.assertEqual("Manufactuer:Energenie Product:R1 MONITOR/CONTROL", Devices.getDescription(0x04,0x02), "")
        self.assertEqual("Manufactuer:Energenie Product:eTRV", Devices.getDescription(0x04,0x03), "")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()