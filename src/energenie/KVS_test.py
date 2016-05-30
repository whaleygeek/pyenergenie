# KVS_test.py  27/05/2016  D.J.Whale
#
# Tester for Key Value Store

import unittest
from lifecycle import *
from KVS import KVS, NotPersistableError

#---- DUMMY TEST CLASSES ------------------------------------------------------

class TV():
    def __init__(self, id):
        print("Creating TV %s" % id)
        self.id = id

    def __repr__(self):
        return "TV(%s)" % self.id

    def get_config(self):
        return {
            "id": self.id
        }

class FACTORY():
    @staticmethod
    def get(name, **kwargs):
        if name == "TV": return TV(**kwargs)
        else:
            raise ValueError("Unknown device name %s" % name)


#----- FILE HELPERS -----------------------------------------------------------

#TODO: This is repeated in Registry_test.py

def remove_file(filename):
    import os
    try:
        os.unlink(filename)
    except OSError:
        pass # ignore

def show_file(filename):
    """Show the contents of a file on screen"""
    with open(filename) as f:
            for l in f.readlines():
                l = l.strip() # remove nl
                print(l)

def write_file(filename, contents):
    with open(filename, "w") as f:
        lines = contents.split("\n")
        for line in lines:
            f.write(line + '\n')


#----- TEST KVS MEMORY --------------------------------------------------------
#
# Test the KVS in-memory only configuration (no persistence to file)

class TestKVSMemory(unittest.TestCase):

    @test_1
    def test_create_blank(self):
        """Create a blank kvs, not bound to any external file"""
        kvs = KVS()
        # it should not fall over

    @test_1
    def test_add(self):
        """Add an object into the kvs store"""
        kvs = KVS()

        kvs["tv1"] = TV(1)
        kvs["tv2"] = TV(2)

        print(kvs.store)

    @test_1
    def test_change(self):
        """Change the value associated with an existing key"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs["tv1"] = TV(111) # change it

        print(kvs.store)

    @test_1
    def test_get(self):
        """Get the object associated with a key in the store"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        t = kvs["tv1"]
        print(t)

    @test_1
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

    @test_1
    def test_size(self):
        """How big is the kvs"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        print(len(kvs))
        kvs["tv2"] = TV(2)
        print(len(kvs))

    @test_1
    def test_keys(self):
        """Get out all keys of the kvs"""
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs["tv2"] = TV(2)
        kvs["tv3"] = TV(3)
        print(kvs.keys())


#----- TEST KVS PERSISTED -----------------------------------------------------
#
# Test the KVS persisted to a file

class TestKVSPersisted(unittest.TestCase):

    KVS_FILENAME = "test.kvs"

    @test_1
    def test_write(self):
        """Write an in memory KVS to a file"""
        remove_file(self.KVS_FILENAME)
        kvs = KVS()
        kvs["tv1"] = TV(1)
        kvs.write(self.KVS_FILENAME)

        show_file(self.KVS_FILENAME)

    @test_1
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

    @test_1
    def test_add(self):
        """Add a new record to a persisted KVS"""
        remove_file(self.KVS_FILENAME)
        kvs = KVS(self.KVS_FILENAME)

        kvs["tv1"] = TV(1)

        print(kvs.store)
        show_file(self.KVS_FILENAME)

    @test_1
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

    @test_1
    def test_change(self):
        """Change an existing record in a persisted KVS"""
        remove_file(self.KVS_FILENAME)
        kvs = KVS(self.KVS_FILENAME)

        kvs["tv1"] = TV(1)
        show_file(self.KVS_FILENAME)

        kvs["tv1"] = TV(2)
        show_file(self.KVS_FILENAME)

    @test_1
    def test_ADD_nofactory(self):
        #NOTE: This is an under the bonnet test of parsing an ADD record from the file

        # No factory callback provided, use ADD parse action
        obj = {
            "type":      "MIHO005",
            "id":        1234
        }
        kvs = KVS(self.KVS_FILENAME)
        kvs.ADD("tv1", obj)

        # expected result: object described as a kvp becomes a kvp in the store if no factory callback
        print(kvs.store)

    @test_1
    def test_ADD_factory(self):
        #NOTE: This is an under the bonnet test of parsing an ADD record from the file
        obj = {
            "type":      "TV",
            "id":        1234
        }
        kvs = KVS(self.KVS_FILENAME)
        kvs.ADD("tv1", obj, create_fn=FACTORY.get)

        # expected result: object described as a kvp becomes a configured object instance in store
        print(kvs.store)


    @test_1
    def test_IGN(self):
        #NOTE: This is an under the bonnet test of parsing an IGN record from the file
        obj = {
            "type":      "TV",
            "id":        1234
        }
        kvs = KVS(self.KVS_FILENAME)
        kvs.IGN("tv1", obj)

        # expected result: no change to the in memory data structures
        print(kvs.store)


    @test_1
    def test_DEL(self):
        #NOTE: This is an under the bonnet test of parsing a DEL record from the file

        #NOTE: This is an under the bonnet test of parsing an IGN record from the file
        obj = {
            "type":      "TV",
            "id":        1234
        }
        kvs = KVS(self.KVS_FILENAME)
        kvs.ADD("tv1", obj)
        kvs.DEL("tv1", obj)

        # expected result: record is deleted from in memory store
        print(kvs.store)


        try:
            kvs.DEL("tv1", obj)
            self.fail("Did not get expected KeyError")
        except KeyError:
            pass # expected
        # expected result: error if it was not in the store in the first place
        print(kvs.store)


    @test_1
    def test_load_process(self):
        """Load and process a file with lots of records in it"""
        CONTENTS = """\
ADD tv
type=TV
id=1

IGN fan
type=TV
id=2

DEL tv

ADD fridge
type=TV
id=99
"""
        write_file(self.KVS_FILENAME, CONTENTS)

        kvs = KVS(self.KVS_FILENAME)
        kvs.load(create_fn=FACTORY.get)

        print(kvs.store)

    @test_1
    def test_not_persistable(self):
        class NPC():
            pass
        remove_file(self.KVS_FILENAME)
        kvs = KVS(self.KVS_FILENAME)

        try:
            kvs["npc"] = NPC() # should throw NotPersistableError
            self.fail("Did not get expected NotPersistableError")
        except NotPersistableError:
            pass # expected


if __name__ == "__main__":
    unittest.main()

# END