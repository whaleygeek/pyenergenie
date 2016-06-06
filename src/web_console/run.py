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

    # Pump receive loop
    #TODO: This will perform really badly, need to probably have a thread doing this
    #when in a web context
    energenie.loop()
    
    # Get readings for any device that can send
    readings = {}
    for name in registry.names():
        c = energenie.registry.peek(name)
        if c.can_send():
            r = c.get_readings_summary()
            readings[name] = r

    return template("device_list", names=registry.names(), readings=readings)


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
    energenie.registry.delete(name)
    return "deleted device %s" % name


#----- APPLICATION STARTUP ----------------------------------------------------

debug(True)
run(port=8081, host="0.0.0.0")

# END
