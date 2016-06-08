# run.py  31/05/2016  D.J.Whale
#
# Run the web_console

from bottle import run, debug, template, get, redirect, request

import energenie
import session


#===== DECORATORS =============================================================
#
# A 'mode' locks users into a specific mode, until they finish it.
# If they try to go to any other mode locked page, they get redirected back
# to the current active mode URL. The URL is stored in a 'mode' session variable.

#TODO: Might put this in session module and push upstream to our bottle cms project

def enforce_mode(m):
    """Redirect to mode handler, if one is active in the session"""
    def inner(*args, **kwargs):
        # get any current mode
        s = session.get_store()
        try:
            mode = s.get("mode")
        except KeyError:
            # mode is not defined
            return m(*args, **kwargs) # just call method unmodified

        # mode is defined
        if request.url == mode:
            # already at the right place
            return m(*args, **kwargs) # just call the method unmodified
        # if not in the right place, send redirect to the mode handler URL
        redirect(mode)

    return inner


def set_mode(s, url=None):
    """Set a mode URL to use for redirects"""
    if url == None:
        url = request.url # assume we are in the handler for the mode already
    s.set("mode", url)


def clear_mode(s):
    """Clear any mode URL to prevent mode redirects"""
    s.delete("mode")


@get('/mode/-')
@session.required
def do_mode_finished(s):
    clear_mode(s)
    return "mode finished"


#===== URL HANDLERS ===========================================================

#----- USER FACING HANDLERS ---------------------------------------------------

# default session state brings user here
@get('/')
@session.needed
def do_home(s):
    """Render the home page"""
    return template('home')


is_receiving = False

@get('/list')
@session.needed
@enforce_mode
def do_list(s):

    # first do a receive poll, to process any data that might have come in.
    # This means all the client has to do is refresh the page to get new data.
    # Re-entrancy trap, although web server is single threaded at moment
    global is_receiving
    if not is_receiving:
        is_receiving = True
        energenie.loop() # allow any messages to arrive
        is_receiving = False

    # Now read out and render the registry
    try:
        registry = s.get("registry")
    except KeyError:
        # Try to make this as safe as possible, only init on very first use
        if energenie.registry == None:
            energenie.init()
        registry = energenie.registry
        s.set("registry", registry)

    # Get readings for any device that can send
    # If we are not watching it yet, turn watch on (by using registry.get())
    readings = {}
    for name in registry.names():
        # are we watching the device?
        if not s.has_key("device.%s" % name):
            # no, so put a watch on it
            d = registry.get(name)
            s.set("device.%s" % name, d)
        else:
            # yes, see if it has any readings
            c = energenie.registry.peek(name)
            if c.can_send():
                r = c.get_readings_summary()
                readings[name] = r

    return template("device_list", names=registry.names(), readings=readings)


@get('/edit/<name>')
@session.required
@enforce_mode
def do_edit(s, name):
    return template("edit", name=name)


@get('/discovery/<type>')
@session.required
def do_discovery(s, type):

    if type == "auto":
        energenie.discovery_auto()
    elif type == "autojoin":
        energenie.discovery_autojoin()
    else:
        energenie.discovery_none()
        type = "none"

    return "Discovery changed to %s" % type


#----- NON USER FACING HANDLERS -----------------------------------------------

@get('/switch_device/<name>/<state>')
@session.required
def do_switch_device(s, name, state):
    ci = energenie.registry.get(name)
    state = state.upper()
    if state in ['1','YES', 'Y', 'TRUE', 'T', 'ON']:
        state = True
    else:
        state = False
    ci.set_switch(state)
    return "device %s switched to:%s" % (name, state)


@get('/rename_device/<old_name>/<new_name>')
@session.required
def do_rename_device(s, old_name, new_name):
    energenie.registry.rename(old_name, new_name)
    return "renamed device %s as %s" % (old_name, new_name)


@get('/delete_device/<name>')
@session.required
def do_delete_device(s, name):
    energenie.registry.delete(name)
    return "deleted device %s" % name


#----- LEGACY LEARN -----------------------------------------------------------

# A much simpler legacy_learn, not a mode, but just driven by the user

@get('/legacy_learn')
@session.required
def legacy_learn(s):
    return template('legacy_learn')


@get('/legacy_learn/on/<house_code>/<device_index>')
@session.required
def legacy_learn_on(s, house_code, device_index):
    ##print("legacy(%s %s ON)" % (house_code, device_index))
    house_code = int(house_code, 16)
    device = energenie.Devices.MIHO008((house_code, device_index))
    device.turn_on()
    return template('legacy_learn', house_code=house_code, device_index=device_index, state='ON')


@get('/legacy_learn/off/<house_code>/<device_index>')
@session.required
def legacy_learn_off(s, house_code, device_index):
    ##print("legacy(%s %s OFF)" % (house_code, device_index))
    house_code = int(house_code, 16)
    device = energenie.Devices.MIHO008((house_code, device_index))
    device.turn_off()
    return template('legacy_learn', house_code=house_code, device_index=device_index, state='OFF')


#===== MODES ==================================================================
#
# A 'mode' is something you can lock the user into
# trying to go to any other mode locked page, will redirect back here

#TODO: Always log to csv file, give user a download option
#TODO: Might pass new messages since last poll in /list update
#if logging is turned on. Will mean that only those messages received
#in last poll will be rendered, but that might be good enough to avoid
#using any ajax or jquery and keep this MVP a really simple building
#block for others to improve on.


#----- LOGGER MODE ------------------------------------------------------------

# NOT DONE YET

@get('/logger')
@session.required
@enforce_mode
def do_logger(s):
    set_mode(s) # sets it to here
    return """
    Should now be locked into logger mode
    <a href='/mode/-'>FINISH</a>
    """
    # start listening
    #   page refreshes every few seconds with any new details
    #   button to stop logging (but if come back to website, this is the page you get)


#----- APPLICATION STARTUP ----------------------------------------------------

debug(True)
run(port=8081, host="0.0.0.0")

# END
