import os
import json
from pyramid.config import Configurator


def dbsetting():
    DOTCLOUD_ENV_FILE = "/home/dotcloud/environment.json"
    if os.path.exists(DOTCLOUD_ENV_FILE):
        with open(DOTCLOUD_ENV_FILE) as f:
            env = json.load(f)
            host = env['DOTCLOUD_DB_MYSQL_HOST']
            user = env['DOTCLOUD_DB_MYSQL_LOGIN']
            passwd = env['DOTCLOUD_DB_MYSQL_PASSWORD']
            port = int(env['DOTCLOUD_DB_MYSQL_PORT'])

        db = {'host': host,
              'user': user,
              'passwd': passwd,
              'port': port}
    else:
        # this is for local
        db = {'read_default_file': '/'.join([os.environ.get('HOME', '~'),
                                             ".my.cnf"]) }

    db['db'] = 'lahman591'
    return db


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['db'] = dbsetting()
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('prbt', '/prbt/{yearID}/{teamID}')
    config.scan()
    return config.make_wsgi_app()
