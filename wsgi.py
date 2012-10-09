#import os.path
import os
from pyramid.scripts.pserve import cherrypy_server_runner
#from pyramid.paster import get_app
from paste.deploy import loadapp

#application = get_app(os.path.join(os.path.dirname(__file__),
#                                   'production.ini'))

current_dir = os.getcwd()
application = loadapp('config:production.ini', relative_to=current_dir)

if __name__ == "__main__":
    cherrypy_server_runner(application, host="0.0.0.0")
