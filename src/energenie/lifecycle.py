# lifecycle.py  21/05/2016  D.J.Whale
#
# Coding lifecycle method decorators.

def unimplemented(m):
    print("warning: unimplemented method %s" % str(m))
    def inner(*args, **kwargs):
        print("warning: unimplemented method %s" % str(m))
        return m()
    return inner

def disabled(m):
    """Load-time waring about disabled function"""
    print("warning: method is disabled:%s" % m)
    def nothing(*args, **kwargs):pass
    return nothing

def untested(m):
    print("warning: untested method %s" % str(m))
    return m

def log_method(m):
    def inner(*args, **kwargs):
        print("CALL %s with: %s %s" % (m, args, kwargs))
        r = m(*args, **kwargs)
        print("RETURN %s with: %s" % (m, r))
        return r
    return inner

def deprecated(m):
    print("warning: deprecated method %s" % str(m))
    return m

# END



