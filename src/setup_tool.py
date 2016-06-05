# setup_tool.py  28/05/2016  D.J.Whale
#
# A simple menu-driven setup tool for the Energenie Python library.
#
# Just be a simple menu system.
#   This then means you don't have to have all this in the demo apps
#   and the demo apps can just refer to object variables names
#   from an assumed auto_create registry, that is built using this setup tool.


import time
import energenie
##from energenie.lifecycle import *


#===== GLOBALS =====

quit = False


#===== INPUT METHODS ==========================================================

try:
    readin = raw_input # Python 2
except NameError:
    readin = input # Python 3


def get_house_code():
    """Get a house code or default to Energenie code"""

    while True:
        try:
            hc = readin("House code (ENTER for default)? ")
            if hc == "": return None

        except KeyboardInterrupt:
            return None # user abort

        try:
            house_code = int(hc, 16)
            return house_code

        except ValueError:
            print("Must enter a number")


def get_device_index():
    """get switch index, default 1 (0,1,2,3,4)"""

    while True:
        try:
            di = readin("Device index 1..4 (ENTER for all)? ")
        except KeyboardInterrupt:
            return None # user abort

        if di == "": return 0 # ALL
        try:
            device_index = int(di)
            return device_index

        except ValueError:
            print("Must enter a number")


def show_registry():
    """Show the registry as a numbered list"""

    i=1
    names = []
    for name in energenie.registry.names():
        print("%d. %s %s" % (i, name, energenie.registry.get(name)))
        names.append(name)
        i += 1

    return names


def get_device_name():
    """Give user a list of devices and choose one from the list"""

    names = show_registry()

    try:
        while True:
            i = readin("Which device %s to %s? " % (1, len(names)))
            try:
                device_index = int(i)
                if device_index < 1 or device_index > len(names):
                    print("Choose a number between %s and %s" % (1, len(names)))
                else:
                    break # got it
            except ValueError:
                print("Must enter a number")

    except KeyboardInterrupt:
        return None # nothing chosen, user aborted

    name = names[device_index-1]
    print("selected: %s" % name)

    return name


#===== ACTION ROUTINES ========================================================

def do_legacy_learn():
    """Repeatedly broadcast a legacy switch message, so you can learn a socket to the pattern"""

    # get device
    house_code = get_house_code()
    device_index = get_device_index()
    # Use a MiHomeLight as it has the longest TX time
    device = energenie.Devices.MIHO008((house_code, device_index))

    # in a loop until Ctrl-C
    print("Legacy learn broadcasting, Ctrl-C to stop")
    try:
        while True:
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
    energenie.discovery_ask(energenie.ask)
    try:
        while True:
            energenie.loop() # Allow receive processing
            time.sleep(0.25) # tick fast enough to get messages in quite quickly

    except KeyboardInterrupt:
        print("Discovery stopped")


def do_list_registry():
    """List the entries in the registry"""

    print("REGISTRY:")
    show_registry()
    energenie.registry.fsk_router.list()


def do_switch_device():
    """Turn the switch on a socket on and off, to test it"""

    global quit

    name = get_device_name()
    device = energenie.registry.get(name)

    def on():
        print("Turning on")
        device.turn_on()

    def off():
        print("Turning off")
        device.turn_off()

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


def do_show_device_status():
    """Show the readings associated with a device"""

    name = get_device_name()
    device = energenie.registry.get(name)

    readings = device.get_readings_summary()
    print(readings)


def do_watch_devices():
    """Repeatedly show readings for all devices"""

    print("Watching devices, Ctrl-C to stop")
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


def do_rename_device():
    """Rename a device in the registry to a different name"""

    # This is useful when turning auto discovered names into your own names

    old_name = get_device_name()
    if old_name == None: return # user abort

    try:
        new_name = readin("New name? ")
    except KeyboardInterrupt:
        return # user abort

    energenie.registry.rename(old_name, new_name)
    print("Renamed OK")


def do_delete_device():
    """Delete a device from the registry so it is no longer recognised"""

    name = get_device_name()
    if name == None: return #user abort

    energenie.registry.delete(name)
    print("Deleted OK")


def do_logging():
    """Enter a mode where all communications are logged to screen and a file"""

    import Logger

    # provide a default incoming message handler for all fsk messages
    def incoming(address, message):
        print("\nIncoming from %s" % str(address))
        print(message)
        Logger.logMessage(message)
    energenie.fsk_router.when_incoming(incoming)

    print("Logging enabled, Ctrl-C to stop")
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


#===== MENU ===================================================================

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
            choice = readin("Choose %d to %d? " % (first, last))
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


#===== MAIN PROGRAM ===========================================================

def setup_tool():
    """The main program loop"""

    while not quit:
        print("\nMAIN MENU")
        show_menu(MAIN_MENU)
        choice = get_choice((1,len(MAIN_MENU)))
        if not quit:
            print("\n")
            handle_choice(MAIN_MENU, choice)


if __name__ == "__main__":

    energenie.init()
    try:
        setup_tool()
    finally:
        energenie.finished()


# END


