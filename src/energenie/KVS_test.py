# KVS_test.py  27/05/2016  D.J.Whale
#
# Tester for Key Value Store

import unittest
from lifecycle import *


class TestKVSMemory(unittest.TestCase):
    pass #TODO

    # create blank
    # add
    # get
    # delete
    # get size
    # get keys

class TestKVSPersisted(unittest.TestCase):
    pass #TODO

    # persist non persisted KVS
    # create from file and load
    # add (does persistent version change)
    # delete (does persistent version change)
    # reload with IGN records
    # reload with DEL records
    # rewrite to a new file


if __name__ == "__main__":
    unittest.main()

# END