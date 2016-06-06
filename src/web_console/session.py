# session.py  22/04/2016  D.J.Whale
#
# A simple in-memory session
#
# TODO: This won't work with a WSGI served app, as there is no stored state
# between requests. Session data must therefore be persisted to the database
# when moving to a WSGI container.


import random
from bottle import request, response, get


#---- SIMPLE SESSION MANAGEMENT -----------------------------------------------

# This implements volatile sessions

COOKIE_SESSION_ID = "sid"

session_store = {} # sessionid(str(int))->SessionStore

def new_id():
    while True:
        r = str(random.randint(1, 100000000))
        if not session_store.has_key(r):
            session_store[r] = ""
            return r


def get_id():
    try:
        return request.get_cookie(COOKIE_SESSION_ID)
    except ValueError:
        return None


def get_store_for(id, create=False):
    # This might fail if session has expired or server reset occured
    try:
        return session_store[id]
    except KeyError:
        if create == False:
            raise KeyError("No session store for id %s" % str(id))
        else:
            s = SessionStore(id)
            session_store[id] = s
            return s



def get_store():
    session_id = get_id()
    return get_store_for(session_id)


def set_id(id):
    s = SessionStore(id)
    session_store[id] = s
    response.set_cookie(COOKIE_SESSION_ID, str(id), path='/')
    return s


def delete_id():
    # Try to remove any objects associated with this session
    try:
        session_id = request.get_cookie(COOKIE_SESSION_ID)
        try:
            del session_store[session_id]
        except KeyError:
            pass

    except ValueError:
        pass

    # Try to force the browser to remove the sessionid reference
    try:
        response.delete_cookie(COOKIE_SESSION_ID, path='/')
    except:
        pass


#----- SIMPLE SESSION OBJECT STORE --------------------------------------------
# This implements volatile objects associated with a session
# each object has a key and a value, and is stored against the sessionid object

# Note this wrapping interface is used, so that we can repurpose this to a persistent
# store with additional error checking included later (e.g. stored in a database or a file)

class SessionStore:
    def __init__(self, session_id):
        self.session_id = session_id
        self.store = {} # key(str)->value(object)

    def __repr__(self):
        return "SessionStore(%s)" % str(self.store)

    #TODO: add Python v=read[k] and write[k=n] and del k methods

    def has_key(self, key): # -> boolean
        """Does the session store for this sessionid contain this key?"""
        return self.store.has_key(key)

    def get(self, key, create=None): # -> object or exception
        """Get the object for this key, throw exception if missing"""
        # if 'create' provided, use this to create a new one
        if not key in self.store:
            if create == None:
                raise KeyError(key)
            else:
                v = create()
                self.store[key] = v
        else:
            v = self.store[key]
        return v


    def delete(self, key):
        """Delete the key and object associated with it"""
        del self.store[key]

    def set(self, key, value):
        """Store a new value against a key, creating key if non existent"""
        self.store[key] = value

    def keys(self):
        return self.store.keys()

    def clear(self):
        """Clear all objects from the object store for this sessionid"""
        self.store = {}


#----- DECORATORS -------------------------------------------------------------
#Look at the code we would need to put into session_required so that it
#always gets the session id if it exists, invalidates it if it is old,
#and creates a new one if needed.

# could get a SessionStore() object and pass it in as session parameter.
# If there is not one, it could create it and push the cookie to the response
# for us (assuming we are using cookies to push the session, as it could
# be done in multiple ways)

def required(method):
    """Asserts that there is a valid session, and gets it"""
    def inner(*args, **kwargs):
        # try to get session id (get_id)
        ##print("SESSION CHECK")
        id = get_id()
        if id == None:
            raise RuntimeError("I expected a session, there is none")

        # get the store associated with this id
        s = get_store_for(id)
        if s == None:
            raise RuntimeError("I expected a session store for id %s, there was none" % id)

        # Pass in session store as new first argument
        return method(s, *args, **kwargs)

    return inner


def needed(method):
    """Checks if there is a valid session, uses it, or creates new one"""
    def inner(*args, **kwargs):
        ##print("SESSION CHECK")
        # try to get session id (get_id)
        id = get_id()
        if id != None:
            s = get_store_for(id, create=True)
        else:
            # There is no session/store, so create it first
            id = new_id()
            s = set_id(id)

        return method(s, *args, **kwargs)

    return inner


#----- URLS FOR SESSION TESTER ------------------------------------------------

SESSION_URL = '/session/'

@get(SESSION_URL) # list
@needed
def do_session_list(s):
    k = s.keys()
    return "LIST %s" % str(k) # TODO template with clickable links to get


@get(SESSION_URL+'<key>/-') # del
@required
def do_session_del(s, key):
    s.delete(key)
    return "DELETED %s" % key # TODO template


@get(SESSION_URL+'-') # clear
@required
def do_session_clear(s):
    s.clear()
    return "CLEARED" # TODO template


@get(SESSION_URL+'<key>/<value>') # set
@needed
def do_session_set(s, key, value):
    s.set(key, value)
    return "SET %s=%s" % (key, value) # TODO template


@get(SESSION_URL+'<key>') # get
@needed
def do_session_get(s, key):
    v = s.get(key)
    return "GET %s=%s" % (key, str(v)) # TODO template to show key and value

# END
