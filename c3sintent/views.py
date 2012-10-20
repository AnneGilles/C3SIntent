# -*- coding: utf-8 -*-

from c3sintent.utils import (
    generate_pdf,
    accountant_mail,
    )
from pkg_resources import resource_filename
import colander
import deform
from deform import ValidationFailure

from pyramid.i18n import (
    #TranslationStringFactory,
    get_localizer,
    get_locale_name,
    )
from pyramid.view import view_config
from pyramid.threadlocal import get_current_request
from pyramid_mailer import get_mailer
from pyramid.httpexceptions import HTTPFound

from translationstring import TranslationStringFactory

deform_templates = resource_filename('deform', 'templates')
c3sintent_templates = resource_filename('c3sintent', 'templates')

my_search_path = (deform_templates, c3sintent_templates)

_ = TranslationStringFactory('C3Sintent')


def translator(term):
    #print("=== this is def translator")
    return get_localizer(get_current_request()).translate(term)

my_template_dir = resource_filename('c3sintent', 'templates/')
deform_template_dir = resource_filename('deform', 'templates/')

zpt_renderer = deform.ZPTRendererFactory(
    [
        my_template_dir,
        deform_template_dir,
        ],
    translator=translator,
    )
# the zpt_renderer above is referred to within the demo.ini file by dotted name

DEBUG = False


@view_config(renderer='templates/disclaimer.pt',
             route_name='disclaimer')
def show_disclaimer(request):

    if hasattr(request, '_REDIRECT_'):
        #from pyramid.httpdexceptions import HTTPFound
        return HTTPFound(location=request.route_url('disclaimer'),
                         headers=request.response.headers)
#    locale_name = get_locale_name(request)
    # check if user clicked on language symbol to have page translated

#    if (request.query_string == '_LOCALE_=%s' % (locale_name)) or (
#        request.query_string == 'l=%s' % (locale_name)):
        # set language cookie
#        request.response.set_cookie('_LOCALE_', locale_name)
#        return HTTPFound(location=request.route_url('disclaimer'),
#                         headers=request.response.headers)

    return {'foo': 'bar'}  # dummy values: template contains all text


@view_config(renderer='templates/intent.pt',
             route_name='intent')
def declare_intent(request):

    # if another language was chosen by clicking on a flag
    # the add_locale_to_cookie subscriber has planted an attr on the request
    if hasattr(request, '_REDIRECT_'):
        #print("request._REDIRECT_: " + str(request._REDIRECT_))

        _query = request._REDIRECT_
        #print("_query: " + _query)
        # set language cookie
        request.response.set_cookie('_LOCALE_', _query)
        request._LOCALE_ = _query
        locale_name = _query
        #print("locale_name (from query_string): " + locale_name)
        from pyramid.httpexceptions import HTTPFound
        #print("XXXXXXXXXXXXXXX ==> REDIRECTING ")
        return HTTPFound(location=request.route_url('intent'),
                         headers=request.response.headers)
    # # if another language was chosen, pick it
    # if request._REDIRECT_ is not '':
    #     print("request.query_string: " + str(request.query_string))
    #     _query = request.query_string
    #     print("_query: " + _query)
    #     # set language cookie
    #     request.response.set_cookie('_LOCALE_', _query)
    #     request._LOCALE_ = _query
    #     locale_name = _query
    #     print("locale_name (from query_string): " + locale_name)
    #     from pyramid.httpexceptions import HTTPFound
    #     print("XXXXXXXXXXXXXXX ==> REDIRECTING ")
    #     return HTTPFound(location=request.route_url('intent'),
    #                      headers=request.response.headers)
    else:
        #locale_name = request._LOCALE_
        locale_name = get_locale_name(request)
        #print("locale_name (from request): " + locale_name)

    # check if user clicked on language symbol to have page translated
    # #print("request.query_string: " + str(request.query_string))
    # if 'l' in request.query_string:
    #     print("request.query_string: " + str(request.query_string))
    #     print("request.query_string[0]: " + str(request.query_string[0]))

    # from pyramid.httpexceptions import HTTPFound
    # if (request.query_string == '_LOCALE_=%s' % (locale_name)) or (
    #     request.query_string == 'l=%s' % (locale_name)):
    #     # set language cookie
    #     request.response.set_cookie('_LOCALE_', locale_name)
    #     return HTTPFound(location=request.route_url('intent'),
    #                      headers=request.response.headers)

    if DEBUG:  # pragma: no cover
        print "-- locale_name: " + str(locale_name)

    country_codes = [
        ('AT', _(u'Austria')),
        ('BE', _(u'Belgium')),
        ('BG', _(u'Bulgaria')),
        ('CH', _(u'Switzerland')),
        ('CZ', _(u'Czech Republic')),
        ('DE', _(u'Germany')),
        ('DK', _(u'Denmark')),
        ('ES', _(u'Spain')),
        ('EE', _(u'Estonia')),
        ('FI', _(u'Finland')),
        ('FR', _(u'France')),
        ('GB', _(u'United Kingdom')),
        ('GR', _(u'Greece')),
        ('HU', _(u'Hungary')),
        ('HR', _(u'Croatia')),
        ('IL', _(u'Israel')),
        ('IE', _(u'Ireland')),
        ('IT', _(u'Italy')),
        ('LT', _(u'Lithuania')),
        ('LV', _(u'Latvia')),
        ('LU', _(u'Luxembourg')),
        ('MT', _(u'Malta')),
        ('NL', _(u'Netherlands')),
        ('PL', _(u'Poland')),
        ('PT', _(u'Portugal')),
        ('SK', _(u'Slovakia')),
        ('SI', _(u'Slovenia')),
        ('SE', _(u'Sweden'))
        ]

   # set default of Country select widget according to locale
    LOCALE_COUNTRY_MAPPING = {
        'de': 'DE',
        'da': 'DK',
        'en': 'GB',
        'es': 'ES',
        'fr': 'FR',
        }
    country_default = LOCALE_COUNTRY_MAPPING.get(locale_name)
    if DEBUG:  # pragma: no cover
        print("== locale is :" + str(locale_name))
        print("== choosing :" + str(country_default))

    class DeclarationOfIntent(colander.MappingSchema):
        """
        colander schema for declaration of intent/ application form
        """
        firstname = colander.SchemaNode(colander.String(),
                                       title=_(u"First Name"))
        lastname = colander.SchemaNode(colander.String(),
                                       title=_(u"Last Name"))
        type_of_creator = (('composer', _(u'composer')),
                           ('lyricist', _(u'lyricist')),
                           ('musician', _(u'musician')),
                           ('music producer', _(u'music producer')),
                           ('remixer', _(u'remixer')),
                           ('dj', _(u'DJ')))

        activity = colander.SchemaNode(
            deform.Set(),
            title=_(
                u'Yes, I am musically active as a '
                '(multiple selection possible)'),
            widget=deform.widget.CheckboxChoiceWidget(values=type_of_creator))

        yes_no = (('yes', _(u'Yes')),
                  ('no', _(u'No')))

        at_least_three_works = colander.SchemaNode(
            colander.String(),
            title=_(u'I have been the (co-)creator of at least three titles '
                    'in one of the functions mentioned under (1)'),
            validator=colander.OneOf([x[0] for x in yes_no]),
            widget=deform.widget.RadioChoiceWidget(values=yes_no))
        member_of_colsoc = colander.SchemaNode(
            colander.String(),
            title=_(u'I am a member of a collecting society.'),
            validator=colander.OneOf([x[0] for x in yes_no]),
            widget=deform.widget.RadioChoiceWidget(values=yes_no),
            )
        email = colander.SchemaNode(colander.String(),
                                    title=_(u'Email'),
                                    validator=colander.Email())
        address1 = colander.SchemaNode(colander.String(),
                                       title=_(u'Street & No.'))
        address2 = colander.SchemaNode(colander.String(),
                                       missing=unicode(''),
                                       title=_(u"address cont'd"))
        postCode = colander.SchemaNode(colander.String(),
                                       title=_(u'Post Code'))
        city = colander.SchemaNode(colander.String(),
                                   title=_(u'City'))
        region = colander.SchemaNode(
            colander.String(),
            title=_(u'Federal State / Province / County'),
            missing=unicode(''))
        country = colander.SchemaNode(colander.String(),
                                      title=_(u'Country'),
                                      default=country_default,
                                      widget=deform.widget.SelectWidget(
                values=country_codes),)
        #print(country_codes())
        understood_declaration = colander.SchemaNode(
            colander.String(),
            title=_(u'I have read and understood the text of the '
                    'declaration of intent.'),
#            validator=colander.OneOf(),
            widget=deform.widget.CheckboxChoiceWidget(
                values=(('yes', _(u'Yes')),)),
            )
        consider_joining = colander.SchemaNode(
            colander.String(),
            title=_(u'I seriously consider to join the C3S and want to '
                    'be notified via e-mail about its foundation.'),
#            validator=colander.OneOf([x[0] for x in yes_no]),
            widget=deform.widget.CheckboxChoiceWidget(
                values=(('yes', _(u'Yes')),)),
            )
        noticed_dataProtection = colander.SchemaNode(
            colander.String(),
            title=_(u'I have taken note of the Data Protection Declaration '
                    'which is part of this text and can be read separately '
                    'at http://www.c3s.cc/disclaimer-en.html and agree with '
                    'it. I know that I may revoke this consent at any time.'),
#            validator=colander.OneOf([x[0] for x in yes_no]),
            widget=deform.widget.CheckboxChoiceWidget(
                values=(('yes', _(u'Yes')),)),
            )
        _LOCALE_ = colander.SchemaNode(colander.String(),
                                       widget=deform.widget.HiddenWidget(),
                                       default=locale_name)

    schema = DeclarationOfIntent()

    form = deform.Form(schema,
                       buttons=[deform.Button('submit', _(u'Submit'))],
                       use_ajax=True,
                       renderer=zpt_renderer
                       )

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            if DEBUG:  # pragma: no cover
                print(appstruct)
        except ValidationFailure, e:
            print(e)
            #message.append(
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            return{'form': e.render()}

        # send mail to accountants // prepare a mailer
        mailer = get_mailer(request)
        # prepare mail
        the_mail = accountant_mail(appstruct)
        mailer.send(the_mail)

        return generate_pdf(appstruct)

    html = form.render()

    return {'form': html}
