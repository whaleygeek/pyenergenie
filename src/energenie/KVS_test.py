# KVS_test.py  27/05/2016  D.J.Whale
#
# Tester for Key Value Store

import unittest
from lifecycle import *
from KVS import KVS

# A dummy test class

class TV():
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "TV(%s)" % self.id


class TestKVSMemory(unittest.TestCase):

    @test_0
    def test_create_blank(self):
        """Create a blank kvs, not bound to any external file"""
        kvs = KVS()
        # it should not fall over

    @test_0
    def test_add(self):
        """Add an object into the kvs store"""
        kvs = KVS()

        kvs["tv1"] = TV(1)
        kvs["tv2"] = TV(2)

        print(kvs.store)

    @test_0
    def test_change(self):
        """Change the value associated with an existing key"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs["tv1"] = TV(111) # change it

        print(kvs.store)

    @test_0
    def test_get(self):
        """Get the object associated with a key in the store"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        t = kvs["tv1"]
        print(t)

    @test_0
    def test_delete(self):
        """Delete an existing key in the store, and a missing key for error"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        del kvs["tv1"]
        print(kvs.store)

        try:
            del kvs["tv1"] # expect error
            self.fail("Did not get expected KeyError exception")
        except KeyError:
            pass # expected

    @test_0
    def test_size(self):
        """How big is the kvs"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        print(len(kvs))
        kvs["tv2"] = TV(2)
        print(len(kvs))

    @test_0
    def test_keys(self):
        """Get out all keys of the kvs"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs["tv2"] = TV(2)
        kvs["tv3"] = TV(3)
        print(kvs.keys())


class TestKVSPersisted(unittest.TestCase):

    @test_0
    def test_write(self):
        pass #TODO: write an in memory kvs to a file
        # write

    @test_0
    def test_load(self):
        pass #TODO: load a blank kvs from an external file
        # load
        # callback for object creation needs to be passed in
        # want to test that kvp's could be used to pass to kwargs to construct
        # data must be passed in string format

    @test_0
    def test_add(self):
        pass #TODO: does persistent version change as well?
        # setitem

    @test_0
    def test_change(self):
        pass #TODO: change the value associated with an existing key

    @test_0
    def test_delete(self):
        pass #TODO: does persistent version get an IGN update?
        # delitem

    @test_0
    def test_IGN(self):
        pass #TODO: do IGN records get ignored?

    @test_0
    def test_DEL(self):
        pass #TODO: do DEL records get processed?


if __name__ == "__main__":
    unittest.main()

# END