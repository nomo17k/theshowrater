import os
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['db'] = {'db': 'lahman591',
                      'read_default_file': '/'.join([os.environ["HOME"],
                                                     ".my.cnf"]) }

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('prbt', '/prbt/{yearID}/{teamID}')
    config.scan()
    return config.make_wsgi_app()
