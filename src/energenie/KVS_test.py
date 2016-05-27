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

    def get_config(self):
        return {
            "id": self.id
        }



def remove_file(filename):
    import os
    os.unlink(filename)


def show_file(filename):
    """Show the contents of a file on screen"""
    with open(filename) as f:
            for l in f.readlines():
                l = l.strip() # remove nl
                print(l)


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

    KVS_FILENAME = "test.kvs"

    @test_0
    def test_write(self):
        """Write an in memory KVS to a file"""
        remove_file(self.KVS_FILENAME)
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs.write(self.KVS_FILENAME)

        show_file(self.KVS_FILENAME)

    @test_0
    def test_load_cache(self):
        """Load record from a kvs file into the kvs cache"""
        # create a file to test against
        remove_file(self.KVS_FILENAME)
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs.write(self.KVS_FILENAME)

        kvs = KVS() # clear it out again

        # load the file
        kvs.load(self.KVS_FILENAME)

        # check the state of the kvs memory
        print(kvs.store)

        # check state of the kvs file at end
        show_file(self.KVS_FILENAME)

    @test_0
    def test_add(self):
        """Add a new record to a persisted KVS"""
        remove_file(self.KVS_FILENAME)
        kvs = KVS(self.KVS_FILENAME)

        kvs["tv1"] = TV(1)

        print(kvs.store)
        show_file(self.KVS_FILENAME)

    @test_0
    def test_delete(self):
        """Delete an existing key from the persistent version"""

        remove_file(self.KVS_FILENAME)
        kvs = KVS(self.KVS_FILENAME)

        kvs["tv1"] = TV(1)
        kvs["tv2"] = TV(2)
        kvs["tv3"] = TV(3)
        kvs["tv4"] = TV(4)

        show_file(self.KVS_FILENAME)

        del kvs["tv1"]

    @test_0
    def test_change(self):
        """Change an existing record in a persisted KVS"""
        remove_file(self.KVS_FILENAME)
        kvs = KVS(self.KVS_FILENAME)

        kvs["tv1"] = TV(1)
        show_file(self.KVS_FILENAME)

        kvs["tv1"] = TV(2) ####HERE###
        show_file(self.KVS_FILENAME)

    #---- HERE ----

    @unimplemented
    @test_1
    def test_ADD(self):
        pass #TODO: do ADD records get added when parsing the file?

    @unimplemented
    @test_0
    def test_IGN(self):
        pass #TODO: do IGN records get ignored when parsing the file?

    @unimplemented
    @test_0
    def test_DEL(self):
        pass #TODO: do DEL records get processed when parsing the file?

    @unimplemented
    @test_0
    def test_load_process(self):
        """Load and process a file with lots of records in it"""
        #including ADD, IGN, DEL
        #make sure callback processing is working too for object creation
        #as the callback will create the object that is stored in the cache
        pass #TODO



if __name__ == "__main__":
    unittest.main()

# END