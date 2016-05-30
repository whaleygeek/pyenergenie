# KVS.py  27/05/2016  D.J.Whale
#
# A generic key value store

##from lifecycle import *

class NotPersistableError(Exception):
    pass

class KVS():
    """A persistent key value store"""
    def __init__(self, filename=None):
        self.filename = filename
        self.store = {}

    def load(self, filename=None, create_fn=None):
        """Load the whole file into an in-memory cache"""

        # use new filename if provided, else use existing filename
        if filename == None:
            filename = self.filename
        if filename == None:
            raise ValueError("No filename specified")

        #TODO: The 'callback' is called to process each record as it is read in??
        # for the Registry, this is a way that it can create the class and also add receive routing

        is_cmd = True
        command = None
        key = None
        obj = None

        ##print("load from %s" % filename)
        with open(filename) as f:
            while True:
                line = f.readline()
                if line == "": # EOF
                    if command != None:
                        self.process(command, key, obj, create_fn)
                    break # END
                else:
                    line = line.strip() # remove nl
                    if is_cmd:
                        if len(line) == 0: # blank
                            pass # ignore extra blank lines
                        else: # not blank
                            # split line, first word is command, second word is the key
                            command, key = line.split(" ", 1)
                            obj = {}
                            is_cmd = False # now in data mode

                    else: # in data mode
                        if len(line) > 0: # not blank
                            ##print("parsing %s" % line)
                            k,v = line.split("=", 1)
                            obj[k] = v
                        else: # is blank
                            self.process(command, key, obj, create_fn)
                            command = None
                            is_cmd = True

        self.filename = filename # remember filename if it was provided

    def process(self, command, key, obj, create_fn):
        """Process the temporary object"""
        m = getattr(self, command)
        #If command is not found? get AttributeError - that's fine
        m(key, obj, create_fn)

    def ADD(self, key, obj, create_fn=None):
        """Add a new item to the kvs"""
        # The ADD command processes the next type= parameter as the class name in context
        # all other parameters are read as strings and passed to class constructor as kwargs

        if create_fn != None:
            ##print("calling create_fn to turn into a class instance")
            type = obj["type"]
            del obj["type"] # don't pass to constructor
            obj = create_fn(type, **obj)
            # If this fails, then this is an error, so just let it bubble out
        else:
            pass ##print("no create_fn configured, just storing kvp")

        ##print("object: %s" % obj)
        # store kvp or class instance appropriately
        self.store[key] = obj

    def IGN(self, key, obj=None, create_fn=None):
        """Ignore the whole record"""
        # The IGN command is the same length as ADD, allowing a seek/write to change any
        # command into IGN without changing the file size, effectively patching the file
        # so that the record is deleted.
        pass # There is nothing to do with this command

    def DEL(self, key, obj=None, create_fn=None):
        """Delete the key from the store"""
        # The DEL command deletes the rec from the store.
        # This is useful to build temporary objects and delete them later.
        # There is no need to write this to the file copy, we're processing the file
        del self.store[key]

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.store:
            self.remove(key) # patches it to an IGN record

        self.store[key] = value
        try:
            obj = value.get_config() # will fail with AttributeError if this method does not exist
        except AttributeError:
            raise NotPersistableError()
        self.append(key, obj)

    def __delitem__(self, key):
        del self.store[key]
        self.remove(key)

    def __len__(self):
        return len(self.store)

    def keys(self):
        return self.store.keys()

    def append(self, key, values):
        """Append a new record to the persistent file"""
        ##print("append:%s %s" % (key, values))

        if self.filename != None:
            with open(self.filename, 'a') as f:
                f.write("\nADD %s\n" % key)
                for k in values:
                    v = values[k]
                    f.write("%s=%s\n" % (k, v))
                f.write("\n")

    def remove(self, key):
        """Remove reference to this key in the file"""
        if self.filename == None:
            return # No file, nothing to do

        with open(self.filename, 'r+') as f: # read and write mode
            while True:
                start = f.tell() # start of current line
                line = f.readline()
                end = f.tell() # position just beyond end of line
                if line == "": break # EOF
                # don't worry about cmd/data, space in search string disambiguates
                if line.startswith("ADD "): # space after is critical to simplify parser
                    line = line.strip() # remove nl
                    cmd, this_key = line.split(" ", 1)
                    if this_key == key:
                        ##print("found: %s %s" % (cmd, this_key))
                        f.seek(start) # back to start of line
                        f.write('IGN') # patch it to be an ignore record but leave record intact
                        f.seek(end) # back to end of line, to process next lines
                        ##print("Patched to IGN rec")

    def write(self, filename=None):
        """Rewrite the whole in memory cache over the top of the external file"""
        #or create a new file if one does not exist

        if filename == None:
            filename = self.filename
        if filename == None:
            raise RuntimeError("No filename configured")

        with open(filename, "w") as f:
            # create an ADD record in the file, for each object in the store

            for key in self.store:
                obj = self.store[key]
                #TODO: for this to work, we need to call the inner object get_config() to get a persistable version
                # that the user of this class can recreate it from later

                f.write("ADD %s\n" % key)
                state = obj.get_config() # will fail if object does not have this method
                for k in state:
                    f.write("%s=%s\n" % (k, state[k]))

                # terminate with a blank line
                f.write("\n")

        self.filename = filename # Remember that we are linked to this file


# END

