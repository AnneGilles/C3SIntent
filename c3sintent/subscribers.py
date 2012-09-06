from pyramid.renderers import get_renderer
from pyramid.i18n import (
    default_locale_negotiator,
    )

from translationstring import TranslationStringFactory

tsf = TranslationStringFactory('C3SIntent')


def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    event.update({'base': base})

BROWSER_LANGUAGES = {
    'de': 'de',
    'de_AT': 'de',
    'de_CH': 'de',
    'de_DE': 'de',
    'en': 'en',
    'en-CA': 'en',
    'en-GB': 'en',
    'en-US': 'en',
    'es': 'es',
    'fr': 'fr',
    # ...
    }


def add_locale_to_cookie(event):
    locale = default_locale_negotiator(event.request)
    #print locale
    if locale is None and event.request.accept_language:
        #print "request.accept_language: " + str(event.request.accept_language)
        #print "locale is None but accept_language exists!"
        locale = event.request.accept_language.best_match(BROWSER_LANGUAGES)
        #print "locale aus accept_language:" + locale
        locale = BROWSER_LANGUAGES.get(locale)
        #print "locale aus BROWSER_LANGUAGES:" + str(locale)
    if locale is None and not event.request.accept_language:
        locale = 'en'

    #print "setting locale: " + str(locale)
    # event.request.cookies['_LOCALE_'] = locale
    event.request.response.set_cookie('_LOCALE_', value=locale)
