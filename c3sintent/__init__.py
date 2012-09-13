from pyramid.config import Configurator
from sqlalchemy import engine_from_config

#from c3sintent.models import initialize_sql
from pyramid_beaker import session_factory_from_settings


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
#   initialize_sql(engine)
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          session_factory=session_factory)

    config.include('pyramid_mailer')
    config.add_translation_dirs(
        'colander:locale/',
        'deform:locale/',
        'c3sintent:locale/')
    config.add_static_view('static',
                           'c3sintent:static', cache_max_age=3600)

    config.add_subscriber('c3sintent.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.add_subscriber('c3sintent.subscribers.add_locale_to_cookie',
                          'pyramid.events.NewRequest')
    # home /
    # membership application form
    config.add_route('intent', '/')

    config.scan()
    return config.make_wsgi_app()
