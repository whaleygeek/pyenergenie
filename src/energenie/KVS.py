# KVS.py  27/05/2016  D.J.Whale
#
# A generic key value store

from lifecycle import *

class KVS():
    """A persistent key value store"""
    def __init__(self, filename=None):
        self.filename = filename
        self.store = {}

    @unimplemented
    def load(self, create_cb):
        """Load the whole file into an in-memory cache"""
        # The 'callback' is called to process each record as it is read in.
        # for the Registry, this is a way that it can create the class and also add receive routing
        pass #TODO
        # open file for read
        # for each line read
        #   if in command mode
        #       if blank line, ignore it
        #       else not blank line
        #           split line, first word is command, second word is the key
        #           remember both
        #           change to data mode
        #   else in data mode
        #       if not blank line
        #           grab key=value
        #           add to temporary object
        #       else blank line
        #           process command,key,values
        # now eof
        #   process command,key,values, if it command is not empty
        # close file

    @unimplemented
    def process(self, command, key, values):
        """Process the temporary object"""
        pass #TODO
        # getattr method associated with the command name, error if no method
        # pass the key,values to that method to let it be processed

    @unimplemented
    def ADD(self, key, values):
        """Add a new item to the kvs"""
        # The ADD command process the next type= parameter as the class name in context
        # all other parameters are read as strings and passed to class constructor as kwargs
        pass #TODO
        # add key=values to the in memory object store
        # open file for append
        # write ADD command with key
        # for all keys in value
        #   write k=v
        # close file

    @unimplemented
    def IGN(self, key, values=None):
        """Ignore the whole record"""
        # The IGN command is the same length as ADD, allowing a seek/write to change any
        # command into IGN without changing the file size, effectively patching the file
        # so that the record is deleted.
        pass # There is nothing to do with this command

    @unimplemented
    def DEL(self, key, values=None):
        """Delete the key from the store"""
        # The DEL command deletes the rec from the store.
        # This is useful to build temporary objects and delete them later.
        # There is no need to write this to the file copy, we're processing the file
        pass #TODO
        # find key in object store, delete it

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value
        self.append(key, value)

    def __delitem__(self, key):
        del self.store[key]
        self.remove(key)

    def __len__(self):
        return len(self.store)

    @untested
    def keys(self):
        return self.store.keys()

    def append(self, key, values):
        """Append a new record to the persistent file"""
        if self.filename != None:
            with open(self.filename, 'a') as f:
                f.write("ADD %s\n" % key)
                for k in values:
                    v = values[k]
                    f.write("%s=%s\n" % (k, v))
                f.write("\n")

    @untested
    def remove(self, key):
        """Remove reference to this key in the file, and remove from in memory store"""
        if self.filename != None:
            pass #TODO
        # open file for read write
        # search line at a time, process each command
        #   when we find the command 'ADD key'
        #   reseek to start of line
        #   write overwrite ADD with IGN
        #   keep going in case of duplicates
        # close file

    @unimplemented
    def write(self, filename=None):
        """Rewrite the whole in memory cache over the top of the external file"""
        # useful if you have updated the in memory copy only and want to completely regenerate
        pass #TODO
        # create file new, for write only
        # for all objects in the store by key
        #   get value
        #   write ADD command key
        #   for all values
        #       write k=v
        #   write blank line
        # close file

# END

