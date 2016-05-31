from bottle import run, debug, template, static_file, error, HTTPError, request, response, post, get

#===== URL HANDLERS ===========================================================

@get('/')
def do_home():
    """Render the home page"""
    return template('home')


#----- APPLICATION STARTUP ----------------------------------------------------

debug(True)
run(port=8081)

# END
