# -*- coding: utf-8 -*-

from c3sintent.utils import (
    generate_pdf,
    accountant_mail,
    )
from pkg_resources import resource_filename
import colander
from webhelpers import constants
import deform
from deform import (
    ValidationFailure,
    #ZPTRendererFactory,
    )

from pyramid.i18n import (
    #TranslationStringFactory,
    get_localizer,
    get_locale_name,
    )
from pyramid.view import view_config
from pyramid.threadlocal import get_current_request
from pyramid_mailer import get_mailer

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


@view_config(renderer='templates/intent.pt',
             route_name='intent')
def declare_intent(request):

    locale_name = get_locale_name(request)

    # check if user clicked on language symbol to have page translated
    #print("request.query_string: " + str(request.query_string))
    from pyramid.httpexceptions import HTTPFound
    if request.query_string == '_LOCALE_=%s' % (locale_name):
        # set language cookie
        request.response.set_cookie('_LOCALE_', locale_name)
        return HTTPFound(location=request.route_url('intent'),
                         headers=request.response.headers)

    if DEBUG:  # pragma: no cover
        print "-- locale_name: " + str(locale_name)

    # set default of Country select widget according to locale
    LOCALE_COUNTRY_MAPPING = {
        'de': 'DE',
        'en': 'GB',
        'fr': 'FR',
        }
    country_default = LOCALE_COUNTRY_MAPPING.get(locale_name)

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
                u'Yes, I am musically active as a ' +
                '(multiple selection possible)'),
            widget=deform.widget.CheckboxChoiceWidget(values=type_of_creator))

        yes_no = (('yes', _(u'Yes')),
                  ('no', _(u'No')))

        at_least_three_works = colander.SchemaNode(
            colander.String(),
            title=_(
                u'I have been the (co-)creator of at least three titles in ' +
                'one of the functions mentioned under (1)'),
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
        country = colander.SchemaNode(colander.String(),
                                      title=_(u'Country'),
                                      default=country_default,
                                      widget=deform.widget.SelectWidget(
                values=constants.country_codes()),)
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
            title=_(u'I seriously consider to join the C3S and want to ' +
                    'be notified via e-mail about its foundation.'),
#            validator=colander.OneOf([x[0] for x in yes_no]),
            widget=deform.widget.CheckboxChoiceWidget(
                values=(('yes', _(u'Yes')),)),
            )
        noticed_dataProtection = colander.SchemaNode(
            colander.String(),
            title=_(u'I have taken note of the Data Protection Declaration ' +
                    'which is part of this text and can be read separately ' +
                    'at http://www.c3s.cc/disclaimer-en.html and agree with ' +
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
            return{'form': e.render(), }

        # send mail to accountants
        mailer = get_mailer(request)

        the_mail = accountant_mail(appstruct)
        mailer.send(the_mail)

        return generate_pdf(appstruct)

    html = form.render()

    return {'form': html, }
