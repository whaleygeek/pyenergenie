# discover_mihome.py  24/05/2016  D.J.Whale
#
# You can discover devices and store them in the registry with setup_tool.py
# However, this is an example of how to do your own discovery using
# one of the built in discovery design patterns.

import energenie

# You could also use the standard energenie.ask callback instead if you want
# as that does exactly the same thing

def ask_fn(address, message):
    MSG = "Do you want to register to device: %s? " % str(address)
    try:
        if message != None:
            print(message)
        y = raw_input(MSG)

    except NameError:
        y = input(MSG)

    if y == "": return True
    y = y.upper()
    if y in ['Y', 'YES']: return True
    return False


def discover_mihome():
    # Select your discovery behaviour from one of these:
    ##energenie.discovery_auto()
    energenie.discovery_ask(ask_fn)
    ##energenie.discovery_autojoin()
    ##energenie.discovery_askjoin(ask_fn)

    # Run the receive loop permanently, so that receive messages are processed
    try:
        print("Discovery running, Ctrl-C to stop")
        while True:
            energenie.loop()

    except KeyboardInterrupt:
        pass # user abort


if __name__ == "__main__":

    print("Starting discovery example")

    energenie.init()

    try:
        discover_mihome()

    finally:
        energenie.finished()


# END

