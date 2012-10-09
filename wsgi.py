# Your WSGI callable should be named “application”, be located in a
# "wsgi.py" file, itself located at the top directory of the service.
#
# For example, to load the app from your "production.ini" file in the same
# directory:
import os.path
from pyramid.scripts.pserve import cherrypy_server_runner
from pyramid.paster import get_app

application = get_app(os.path.join(os.path.dirname(__file__),
                                   'production.ini'))

if __name__ == "__main__":
    cherrypy_server_runner(application, host="0.0.0.0")
