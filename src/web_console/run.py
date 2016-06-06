# run.py  31/05/2016  D.J.Whale
#
# Run the web_console

from bottle import run, debug, template, get

import energenie
import session


#===== URL HANDLERS ===========================================================

# default session state brings user here
@get('/')
def do_home():
    """Render the home page"""
    return template('home')


@get('/list')
@session.needed
def do_list(s):
    try:
        registry = s.get("registry")
    except KeyError:
        # Try to make this as safe as possible, only init on very first use
        if energenie.registry == None:
            energenie.init()
        registry = energenie.registry
        s.set("registry", registry)
    r = {"house": "(house readings here)"} #TODO: map of name to readings summary
    return template("device_list", names=registry.names(), readings=r)


@get('/activate_device/<name>')
@session.required
def do_activate_device(s, name):
    return "TODO: Activate devices %s" % name
    # action to get() the device (remember it is activated in registry??)
    # i.e. when listing registry, need to be able to query if there is a route,
    # and that will mean it is activated)
    # refresh back to list page  (or initiating page in HTTP_REFERRER?)


@get('/deactivate_device/<name>')
@session.required
def do_deactivate_device(s, name):
    return "TODO: Deactivate device %s" % name
    # only allowed on devices that are already activated
    # error if not yet activated
    # ask router to delete the route to the device
    # refresh back to list page  (or initiating page in HTTP_REFERRER?)


@get('/switch_device/<name>/<state>')
@session.required
def do_switch_device(s, name, state):
    return "TODO: Switch device %s" % name
    # name and on/off will be captured from list page
    # both on and off offered in case of catchup, but actual state shown on list
    # change the switch state
    # refresh back to list page (or initiating page in HTTP_REFERRER?)


# session state could lock us here regardless of URL, it is a mode
@get('/legacy_learn')
@session.required
def do_legacy_learn(s):
    return "TODO: legacy learning page - this enters a sticky MODE"
    # collect house code and device index
    # start broadcasting (new page)
    #   button to stop broadcasting (but if come back to web site, this is page you get)
    # stop goes back to list page  (or initiating page in HTTP_REFERRER?)


# session state could lock us here regardless of URL, it is a mode
@get('/mihome_discovery')
@session.required
def do_mihome_discovery(s):
    return "TODO: MiHome discovery page - this enters a sticky MODE"""
    # start listening
    #   page refreshes every few seconds with any new details
    #   button to stop listening (but if come back to website, this is the page you get)
    # stop goes back to list page  (or initiating page in HTTP_REFERRER?)


@get('/logger') # session state could lock us here regardless of URL, it is a mode
@session.required
def do_logger(s):
    return "TODO: Logger page - this enters a sticky MODE"
    # start listening
    #   page refreshes every few seconds with any new details
    #   button to stop logging (but if come back to website, this is the page you get)


@get('/rename_device/<old_name>/<new_name>')
@session.required
def do_rename_device(s, old_name, new_name):
    return "TODO: rename device from %s to %s" % (old_name, new_name)
    # page to get old name is from list, new_name is entered on a page
    #   then kicks an action page to actually do the rename
    #   then refreshes back to the list page (or initiating page in HTTP_REFERRER?)


@get('/delete_device/<name>')
@session.required
def do_delete_device(s, name):
    return "TODO: delete device %s" % name
    # name is passed in from the list page
    # action to delete the item
    # refresh back to the list page (or initiating page in HTTP_REFERRER?)




#----- APPLICATION STARTUP ----------------------------------------------------

debug(True)
run(port=8081)

# END
