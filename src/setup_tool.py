# setup_tool.py  28/05/2016  D.J.Whale
#
# A simple menu-driven setup tool for the Energenie Python library.

# Just be a simple menu system.
#   This then means you don't have to have all this in the demo apps
#   and the demo apps can just refer to object variables names
#   from an assumed auto_create registry, that is built using this setup tool.


import energenie
from energenie.lifecycle import *

#TODO: Catch Ctrl-C interrupt if possible
try:
    readin = raw_input # Python 2
except NameError:
    readin = input # Python 3

quit = False


@log_method
def do_legacy_learn():
    """Repeatedly broadcast a legacy switch message, so you can learn a socket to the pattern"""
    pass #TODO
    # get house code, default to energenie code
    # get switch index, default 1 (0,1,2,3,4)
    # go into transmit OOK mode
    # in a loop until Ctrl-C
    #   transmit on message for house/device
    #   wait a short while


@log_method
def do_mihome_discovery():
    """Discover any mihome device when it sends reports"""
    pass #TODO
    # select join ask discovery mode
    # in a loop until Ctrl-C
    #   just wait, the discovery agent will do everything for us
    #   in discover_askjoin mode, it will even ask the user for registry add/ignore


@log_method
def do_list_registry():
    """List the entries in the registry"""
    energenie.registry.list()


@log_method
def do_rename_device():
    """Rename a device in the registry to a different name"""
    #This is useful when turning auto discovered names into your own names
    #TODO: The registry does not support a rename mode at the moment
    #will need to add this by getting the record, deleting it, and appending it again
    pass #TODO


@log_method
def do_delete_device():
    """Delete a device from the registry so it is no longer recognised"""
    pass #TODO
    #list the registry with numbers
    # get the number of the device to delete, ctrl-C aborts
    # ask the registry to delete it


@log_method
def do_switch_device():
    """Turn the switch on a socket on and off, to test it"""
    pass #TODO
    # select the device from a menu of numbered devices
    # ask user for on/off/another/done
    # if on, turn it on
    # if off, turn it off
    # if another, show list again
    # if done, exit


@log_method
def do_show_device_status():
    """Show the readings associated with a device"""
    pass #TODO
    #TODO, not sure might show all devices in a simple table
    #note different field names make table display hard, unless there are shorthand names
    # for each device in the registry
    #   show a summary line for that device


@log_method
def do_watch_device():
    """Repeatedly show readings for a single device"""
    pass #TODO
    #show a list of devices
    # get a device number from the user
    # loop until Ctrl-C
    #   show device status
    #   wait until device status updates


@log_method
def do_logging():
    """Enter a mode where all communications are logged to screen and a file"""
    pass #TODO
    # loop until Ctrl-C
    #   if a device update comes in
    #   display summary of its data on screen
    #   add summary of data to energenie.csv using Logging.log_message


@log_method
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
    pass


def handle_choice(menu, choice):
    """Route to the handler for the given menu choice"""
    menu[choice-1][1]()


MAIN_MENU = [
    ("legacy learn mode",     do_legacy_learn),
    ("mihome discovery mode", do_mihome_discovery),
    ("list registry",         do_list_registry),
    ("watch device",          do_watch_device),
    ("rename device",         do_rename_device),
    ("delete device",         do_delete_device),
    ("switch device",         do_switch_device),
    ("show device status",    do_show_device_status),
    ("logging",               do_logging),
    ("quit",                  do_quit)
]


def setup_tool():
    while not quit:
        print("MAIN MENU")
        show_menu(MAIN_MENU)
        choice = get_choice((1,len(MAIN_MENU)+1))
        handle_choice(MAIN_MENU, choice)


#----- MAIN ENTRY POINT -------------------------------------------------------

if __name__ == "__main__":
    energenie.init()
    try:
        setup_tool()
    finally:
        energenie.finished()

# END


