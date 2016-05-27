# KVS_test.py  27/05/2016  D.J.Whale
#
# Tester for Key Value Store

import unittest
from lifecycle import *

class TestKVSMemory(unittest.TestCase):

    @test_0
    def test_create_blank(self):
        pass #TODO: create a blank registry not bound to a file
        #init

    @test_0
    def test_add(self):
        pass #TODO: add an object into the store
        #setitem

    @test_0
    def test_change(self):
        pass #TODO: if we change the value associated with a key, does it get updated?
        #setitem

    @test_0
    def test_get(self):
        pass #TODO: get an object by it's key name
        #getitem

    @test_0
    def test_delete(self):
        pass #TODO: delete an object by it's key name
        #delitem

    @test_0
    def test_size(self):
        pass #TODO: how big is the kvs
        # size

    @test_0
    def test_keys(self):
        pass #TODO: get all keys
        # keys

class TestKVSPersisted(unittest.TestCase):

    @test_0
    def test_write(self):
        pass #TODO: write an in memory kvs to a file
        # write

    @test_0
    def test_load(self):
        pass #TODO: load a blank kvs from an external file
        # load

    @test_0
    def test_add(self):
        pass #TODO: does persistent version change as well?
        # setitem

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