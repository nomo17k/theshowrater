import os
import json
from pyramid.config import Configurator


def configure_db():
    """Configure database either locally or on dotCloud."""
    db = {'db': 'lahman591'}
    DOTCLOUD_ENV_FILE = "/home/dotcloud/environment.json"
    if os.path.exists(DOTCLOUD_ENV_FILE):
        # getting here means the app is running on dotCloud.
        with open(DOTCLOUD_ENV_FILE) as f:
            env = json.load(f)
            host = env['DOTCLOUD_DB_MYSQL_HOST']
            user = env['DOTCLOUD_DB_MYSQL_LOGIN']
            passwd = env['DOTCLOUD_DB_MYSQL_PASSWORD']
            port = int(env['DOTCLOUD_DB_MYSQL_PORT'])
        db.update({'host': host, 'user': user, 'passwd': passwd, 'port': port})
    else:
        # running locally
        default_file = '/'.join([os.environ.get('HOME', '~'), ".my.cnf"])
        db.update({'read_default_file': default_file})
    return db


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    settings['db'] = configure_db()
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('prbt', '/prbt')
    config.scan()
    return config.make_wsgi_app()
