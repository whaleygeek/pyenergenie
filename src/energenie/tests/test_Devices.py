# test_Devices.py  13/10/2015  E.D.Hurst-Frost
#
# Devices module tests.
import unittest
from energenie import Devices

class Test_Devices(unittest.TestCase):
    def test_getDescription(self):
        self.assertEqual("Manufactuer:Energenie Product:C1 MONITOR", Devices.getDescription(0x04,0x01))
        self.assertEqual("Manufactuer:Energenie Product:R1 MONITOR/CONTROL", Devices.getDescription(0x04,0x02))
        self.assertEqual("Manufactuer:Energenie Product:eTRV", Devices.getDescription(0x04,0x03))
        self.assertEqual("Manufactuer:Energenie Product:UNKNOWN", Devices.getDescription(0x04,0xff))
        self.assertEqual("Manufactuer:UNKNOWN Product:UNKNOWN", Devices.getDescription(0xff,0x03), "Product ID should be manufacturer specific")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()