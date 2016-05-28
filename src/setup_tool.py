# setup_tool.py  28/05/2016  D.J.Whale
#
# A simple menu-driven setup tool for the Energenie Python library.

# Just be a simple menu system.
#   This then means you don't have to have all this in the demo apps
#   and the demo apps can just refer to object variables names
#   from an assumed auto_create registry, that is built using this setup tool.

# REQUIREMENTS
# - learn mode broadcasts for legacy devices
# - testing legacy device switches by turning on and off
# - assisted join from mihome with add to registry with friendly names
# - showing trace of data coming from mihome monitor
# - turning adaptor plus switch on and off
# - dumping the contents of the registry in a simple format
# - deleting devices from the registry]
# - renaming devices in the registry (e.g. auto learn devices->nice name)

import energenie
from energenie.lifecycle import *

try:
    readin = raw_input # Python 2
except NameError:
    readin = input # Python 3

quit = False


@log_method
def do_legacy_learn():
    pass #TODO


@log_method
def do_mihome_discovery():
    pass #TODO


@log_method
def do_list_registry():
    pass #TODO


@log_method
def do_rename_device():
    pass #TODO


@log_method
def do_delete_device():
    pass #TODO


@log_method
def do_switch_device():
    pass #TODO


@log_method
def do_show_device_status():
    pass #TODO


@log_method
def do_logging():
    pass #TODO


@log_method
def do_quit():
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


