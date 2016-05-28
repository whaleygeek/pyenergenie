# setup_tool.py  28/05/2016  D.J.Whale
#
# A simple menu-driven setup tool for the Energenie Python library.

# Just be a simple menu system.
#   This then means you don't have to have all this in the demo apps
#   and the demo apps can just refer to object variables names
#   from an assumed auto_create registry, that is built using this setup tool.

#TODO: Choose a better way to interrupt other than Ctrl-C
#It's very platform independent
#also, the foreground thread gets the KeyboardInterrupt,
#so as soon as threads are added, its a bad way to terminate user entry
#or processing.

import time
import energenie
from energenie.lifecycle import *

try:
    readin = raw_input # Python 2
except NameError:
    readin = input # Python 3

quit = False


def do_legacy_learn():
    """Repeatedly broadcast a legacy switch message, so you can learn a socket to the pattern"""
    # get house code, default to energenie code
    hc = readin("House code? (ENTER for default) ")
    if hc == "":
        house_code = None
    else:
        house_code = int(hc, 16)
        #TODO: error check

    # get switch index, default 1 (0,1,2,3,4)
    si = readin("Switch index 1..4? (ENTER for all)")
    if si == "":
        switch_index = 0 #ALL
    else:
        switch_index = int(si)
        #TODO: error check

    device = energenie.Devices.ENER002((house_code, switch_index))

    # in a loop until Ctrl-C
    try:
        while True: #TODO: detect Ctrl-C
            print("ON")
            device.turn_on()
            time.sleep(0.5)
            print("OFF")
            device.turn_off()
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass # user exit


def do_mihome_discovery():
    """Discover any mihome device when it sends reports"""
    print("Discovery mode, press Ctrl-C to stop")
    energenie.Registry.discovery_ask(energenie.Registry.ask)
    try:
        while True:
            energenie.loop() # Allow receive processing
            time.sleep(0.25) # tick fast enough to get messages in quite quickly
    except KeyboardInterrupt:
        print("Discovery stopped")


def show_registry():
    """Show the registry as a numbered list"""
    names = energenie.registry.names()
    i=1
    for name in names:
        print("%d. %s %s" % (i, name, energenie.registry.get(name)))
        i += 1
    return names


def do_list_registry():
    """List the entries in the registry"""
    show_registry()


def do_switch_device():
    global quit
    """Turn the switch on a socket on and off, to test it"""

    #TODO DRY name = select_device()
    # select the device from a menu of numbered devices
    names = show_registry()

    # ask user for on/off/another/done
    i = readin("Which device %s to %s" % (1,len(names)))
    device_index = int(i)
    #TODO: error check
    #TODO: Ctrl-C check

    name = names[device_index-1]
    print("selected: %s" % name)

    device = energenie.registry.get(name)
    #TODO: DRY END

    #TODO could list all action methods by introspecting device class
    # and build a device specific menu
    def on():
        print("Turning on")
        device.turn_on

    def off():
        print("Turning off")
        device.turn_off

    MENU = [
        ("on",  on),
        ("off", off)
    ]

    try:
        while not quit:
            show_menu(MENU)
            choice = get_choice((1,len(MENU)))
            if choice != None:
                handle_choice(MENU, choice)
    except KeyboardInterrupt:
        pass # user exit
    quit = False


@untested
def do_show_device_status():
    """Show the readings associated with a device"""

    #TODO DRY name = select_device()
    names = show_registry()

    energenie.loop() # allow receive processing #TODO: not long enough for >1 msg??

    # ask user for on/off/another/done
    i = readin("Which device %s to %s" % (1,len(names)))
    device_index = int(i)
    #TODO: error check
    #TODO: Ctrl-C check

    name = names[device_index-1]
    print("selected: %s" % name)
    device = energenie.registry.get(name)
    #TODO: DRY END

    readings = device.get_readings_summary()
    print(readings)


@untested
def do_watch_devices():
    """Repeatedly show readings for all devices"""
    try:
        while True:
            energenie.loop() # allow receive processing
            print('-' * 80)
            names = energenie.registry.names()
            for name in names:
                device = energenie.registry.get(name)
                readings = device.get_readings_summary()
                print("%s %s" % (name, readings))
            print("")
            time.sleep(1)

    except KeyboardInterrupt:
        pass # user exit


@untested
def do_rename_device():
    """Rename a device in the registry to a different name"""
    #This is useful when turning auto discovered names into your own names

    #TODO DRY name = select_device()
    names = show_registry()

    # ask user for on/off/another/done
    i = readin("Which device %s to %s" % (1,len(names)))
    device_index = int(i)
    #TODO: error check
    #TODO: Ctrl-C check

    name = names[device_index-1]
    print("selected: %s" % name)
    #TODO: DRY END

    new_name = readin("New name?")

    energenie.registry.rename(name, new_name)


@untested
def do_delete_device():
    """Delete a device from the registry so it is no longer recognised"""

    #TODO DRY name = select_device()
    names = show_registry()

    # ask user for on/off/another/done
    i = readin("Which device %s to %s" % (1,len(names)))
    device_index = int(i)
    #TODO: error check
    #TODO: Ctrl-C check

    name = names[device_index-1]
    print("selected: %s" % name)
    #TODO: DRY END

    energenie.registry.delete(name)


@untested
def do_logging():
    """Enter a mode where all communications are logged to screen and a file"""
    import Logger

    # provide a default incoming message handler for all fsk messages
    def incoming(address, message):
        print("\nIncoming from %s" % str(address))
        print(message)
        Logger.logMessage(message)
    energenie.fsk_router.when_incoming(incoming)

    try:
        while True:
            energenie.loop()

    except KeyboardInterrupt:
        pass #user quit

    finally:
        energenie.fsk_router.when_incoming(None)


def do_quit():
    """Finished with the program, so exit"""
    global quit
    quit = True


def show_menu(menu):
    """Display a menu on the console"""
    i = 1
    for item in menu:
        print("%d. %s" % (i, item[0]))
        i += 1


def get_choice(choices):
    """Get and validate a numberic choice from the tuple choices(first, last)"""
    first = choices[0]
    last  = choices[1]
    try:
        while True:
            choice = readin("Choose %d to %d?" % (first, last))
            try:
                choice = int(choice)
                if choice < first or choice > last:
                    print("Must enter a number between %d and %d" % (first, last))
                else:
                    return choice
            except ValueError:
                print("Must enter a number")
    except KeyboardInterrupt:
        do_quit()


def handle_choice(menu, choice):
    """Route to the handler for the given menu choice"""
    menu[choice-1][1]()


MAIN_MENU = [
    ("legacy learn mode",     do_legacy_learn),
    ("mihome discovery mode", do_mihome_discovery),
    ("list registry",         do_list_registry),
    ("switch device",         do_switch_device),
    ("show device status",    do_show_device_status),
    ("watch devices",         do_watch_devices),
    ("rename device",         do_rename_device),
    ("delete device",         do_delete_device),
    ("logging",               do_logging),
    ("quit",                  do_quit)
]


def setup_tool():
    while not quit:
        print("MAIN MENU")
        show_menu(MAIN_MENU)
        choice = get_choice((1,len(MAIN_MENU)))
        if not quit:
            handle_choice(MAIN_MENU, choice)


#----- MAIN ENTRY POINT -------------------------------------------------------

if __name__ == "__main__":
    energenie.init()
    try:
        setup_tool()
    finally:
        energenie.finished()

# END


