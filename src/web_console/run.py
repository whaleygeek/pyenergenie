# run.py  31/05/2016  D.J.Whale
#
# Run the web_console

from bottle import run, debug, template, get

from energenie import Registry


#===== URL HANDLERS ===========================================================

#TODO: Session state, we need a session to store a registry object in,
#that we can use between calls.


# default session state brings user here
@get('/')
def do_home():
    """Render the home page"""
    return template('home')


@get('/list')
def do_list():
    return "TODO: list registry (fix session state first)"
    # list all items in registry
    # buttons for all devices
    #   rename -> rename_device
    #   delete -> delete_device
    #   activate (do a get so it is actively receiving) -> activate_device
    # also for activated devices
    #   shows readings from them
    #   shows present switch state
    #   button to turn switch on and off -> switch_device
    #   button to deactivate (unroute the rx so not receiving any more) -> deactivate_device


# session state could lock us here regardless of URL, it is a mode
@get('/legacy_learn')
def do_legacy_learn():
    return "TODO: legacy learning page"
    # collect house code and device index
    # start broadcasting (new page)
    #   button to stop broadcasting (but if come back to web site, this is page you get)
    # stop goes back to list page  (or initiating page in HTTP_REFERRER?)


# session state could lock us here regardless of URL, it is a mode
@get('/mihome_discovery')
def do_mihome_discovery():
    return "TODO: MiHome discovery page"""
    # start listening
    #   page refreshes every few seconds with any new details
    #   button to stop listening (but if come back to website, this is the page you get)
    # stop goes back to list page  (or initiating page in HTTP_REFERRER?)


@get('/logger') # session state could lock us here regardless of URL, it is a mode
def do_logger():
    return "TODO: Logger page"
    # start listening
    #   page refreshes every few seconds with any new details
    #   button to stop logging (but if come back to website, this is the page you get)


@get('/rename_device/<old_name>/<new_name>')
def do_rename_device(old_name, new_name):
    pass #TODO
    # page to get old name is from list, new_name is entered on a page
    #   then kicks an action page to actually do the rename
    #   then refreshes back to the list page (or initiating page in HTTP_REFERRER?)


@get('/delete_device/<name>')
def do_delete_device(name):
    pass #TODO
    # name is passed in from the list page
    # action to delete the item
    # refresh back to the list page (or initiating page in HTTP_REFERRER?)


@get('/activate_device/<name>')
def do_activate_device(name):
    pass #TODO
    # action to get() the device (remember it is activated in registry??)
    # i.e. when listing registry, need to be able to query if there is a route,
    # and that will mean it is activated)
    # refresh back to list page  (or initiating page in HTTP_REFERRER?)


@get('/deactivate_device/<name>')
def do_deactivate_device(name):
    pass #TODO
    # only allowed on devices that are already activated
    # error if not yet activated
    # ask router to delete the route to the device
    # refresh back to list page  (or initiating page in HTTP_REFERRER?)


@get('/switch_device/<name>/<state>')
def do_switch_device(name, state):
    pass #TODO
    # name and on/off will be captured from list page
    # both on and off offered in case of catchup, but actual state shown on list
    # change the switch state
    # refresh back to list page (or initiating page in HTTP_REFERRER?)


#----- APPLICATION STARTUP ----------------------------------------------------

debug(True)
run(port=8081)

# END
