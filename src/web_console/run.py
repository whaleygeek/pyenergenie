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


@get('/list')
@session.needed
@enforce_mode
def do_list(s):
    try:
        registry = s.get("registry")
    except KeyError:
        # Try to make this as safe as possible, only init on very first use
        if energenie.registry == None:
            energenie.init()
        registry = energenie.registry
        s.set("registry", registry)

    # Get readings for any device that can send
    readings = {}
    for name in registry.names():
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


#----- NON USER FACING HANDLERS -----------------------------------------------

is_receiving = False

@get('/receive_loop')
def do_receive_loop():
    """A cheat's way of pumping the receive loop, for testing"""
    # This will probably be fetched by the javascript on a repeating timer

    #TODO: Need to put a failing lock around this to prevent threading issues in web context
    #web server is single threaded at the moment, so we won't hit this quite yet.

    # Re-entrancy trap
    global is_receiving
    if not is_receiving:
        is_receiving = True
        energenie.loop()
        is_receiving = False
        redirect('/list')
    else:
        redirect('/list?busy')


@get('/watch_device/<name>')
@session.required
def do_watch_device(s, name):
    c = energenie.registry.get(name)
    energenie.fsk_router.list() # to console
    ##TESTING
    ##dummy_payload = {
    ##    "recs":[
    ##        {
    ##            "paramid": energenie.OpenThings.PARAM_DOOR_SENSOR,
    ##            "value": 1
    ##        }
    ##    ]
    ##}
    ##c.handle_message(dummy_payload)
    # Store device class instance in session store, so we can easily get its readings
    s.set("device.%s" % name, c)
    return "Watch is now active for %s" % name


@get('/unwatch_device/<name>')
@session.required
def do_unwatch_device(s, name):
    s.delete("device.%s" % name)
    energenie.registry.unget(name)
    return "Watch is now inactive for %s" % name


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


#===== MODES ==================================================================
#
# A 'mode' is something you can lock the user into
# trying to go to any other mode locked page, will redirect back here


#----- LEGACY LEARN MODE ------------------------------------------------------
# This is a naive client-managed implementation. It pokes the server every few
# seconds to get it to toggle the switch.
# A better implementation would be to start a server thread transmitting
# and provide user with a way to stop that thread via the UI.

#TODO: would this just be better as a non repeating GUI that has
# house code
# device index
# ON OFF buttons??

@get('/legacy_learn')
@session.required
@enforce_mode
def do_legacy_learn(s):
    # show UI
    return """"
    legacy learn mode UI goes here...<BR>
    house code [] device index []<BR>
    <a href="/legacy_learn/run">RUN</a>
    """
    # collect house code and device index
    # start broadcasting (new page)
    #   button to stop broadcasting (but if come back to web site, this is page you get)
    # stop goes back to list page  (or initiating page in HTTP_REFERRER?)


@get('/legacy_learn/run/<house_code>/<device_index>')
@session.required
@enforce_mode
def do_legacy_learn_run(s, house_code, device_index):
    set_mode(s) # sets it to here
    # store house_code and device_index in session 's'
    return """
    Should now be locked into legacy_learn_mode
    <a href='/mode/-'>FINISH</a>
    """
    #TODO: turn on
    #TODO: redirect in 1 sec to turn off


@get('/legacy_learn/run/on')
@session.required
@enforce_mode
def do_legacy_learn_run(s):
    return "should now be ON" #TODO: refresh after 1 sec to OFF
    #TODO: include FINISH link


@get('/legacy_learn/off')
@session.required
@enforce_mode
def do_legacy_learn_run(s):
    # run the monitor - poke the transmitter with toggle ON/OFF with each refresh
    return "Should now be OFF" #TODO: refresh after 1 sec to ON
    #TODO: include FINISH link


#----- MIHOME DISCOVERY MODE --------------------------------------------------

# NOT DONE YET

@get('/mihome_discovery')
@session.required
@enforce_mode
def do_mihome_discovery(s):
    set_mode(s) # sets it to here
    return """
    Should now be locked into mihome discovery mode
    <a href='/mode/-'>FINISH</a>
    """
    # start listening
    #   page refreshes every few seconds with any new details
    #   button to stop listening (but if come back to website, this is the page you get)
    # stop goes back to list page  (or initiating page in HTTP_REFERRER?)


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
