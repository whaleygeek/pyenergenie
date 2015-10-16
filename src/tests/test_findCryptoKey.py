# OpenHEMS.py  16/10/2015  E.D.Hurst-Frost
#
# Brute force search for crypto key

import unittest
from energenie import crypto
from energenie.OpenHEMS import calcCRC

class FindCryptoKey(unittest.TestCase):


    def test_findEncryptId(self):
#         payload = [0x2b,0xfe,0x88,0xd8,0xf0,0xc9,0x6c,0x9,0xa4,0x39,0x18,0xec,0x36,0xd9,0xf6,0xae,0x59,0xd9,0x8e,0xfb,0x8f,0x75,0x7d,0x1a,0xd5,0x20,0x21,0x15,0xdb,0x5,0x79,0x82,0x89,0x40,0xe5,0x8a,0xe9,0x3f,0x70,0xec,0xec,0xd3,0x43,0x4c]
        payload = [0xe,0x4,0x3,0x3b,0x34,0x94,0x14,0xf0,0xf4,0xad,0x67,0x4,0x89,0xe6,0x24]
        
        print("Searching for CRYPT ID...")
        for cryptId in range(0,0xffff):
            p = list(payload)
            encryptPIP = (p[3]<<8) + p[4]
            crypto.init(cryptId, encryptPIP)
            crypto.cryptPayload(p, 5, len(p)-5) # including CRC
            crc_actual  = (p[-2]<<8) + p[-1]
            crc_expected = calcCRC(p, 5, len(p)-(5+2))
            if crc_actual == crc_expected:
                break
            
        self.assertEqual(crc_actual, crc_expected, "CRYPT ID not found")
        print("Found working CRYPTO key %d(0x%x)" % (cryptId,cryptId))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_findEncryptId']
    unittest.main()