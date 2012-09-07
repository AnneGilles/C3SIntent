# -*- coding: utf-8  -*-
import subprocess
from fdfgen import forge_fdf

from pyramid_mailer.message import Message
from pyramid_mailer.message import Attachment

DEBUG = False


def generate_pdf(appstruct):
    """
    this function receives an appstruct
    (a datastructure received via formsubmission)
    and prepares and returns a PDF using pdftk
    """
    DEBUG = True  # False

#     _composer = 'Yes' if appstruct[
#         'activity'].issuperset(['composer']) else 'Off'
#     _musician = 'Yes' if appstruct[
#         'activity'].issuperset(['musician']) else 'Off'
#     _lyricist = 'Yes' if appstruct[
#         'activity'].issuperset(['lyricist']) else 'Off'
#     _producer = 'Yes' if appstruct[
#         'activity'].issuperset(['producer']) else 'Off'
#     _dj = 'Yes' if appstruct[
#         'activity'].issuperset(['dj']) else 'Off'

#    print('---------------')
#    print(appstruct)
#    print('---------------')

# here we gather all information from the supplied data to prepare pdf-filling

    fields = [
        ('Name', appstruct['name']),
        ('streetNo', appstruct['address1']),
        ('address2', appstruct['address2']),
        ('postCodeCity', appstruct['postCodeCity']),
        ('email', appstruct['email']),
        ('country', appstruct['country']),
        ('composer',
         'Yes' if appstruct['activity'].issuperset(['composer']) else 'Off'),
        ('lyricist',
         'Yes' if appstruct['activity'].issuperset(['lyricist']) else 'Off'),
        ('musician',
         'Yes' if appstruct['activity'].issuperset(['musician']) else 'Off'),
        ('producer',
         'Yes' if appstruct['activity'].issuperset(
                ['music producer']) else 'Off'),
        ('remixer',
         'Yes' if appstruct['activity'].issuperset(['remixer']) else 'Off'),
        ('dj',
         'Yes' if appstruct['activity'].issuperset(['dj']) else 'Off'),
        ('YesDataProtection',
         'Yes' if appstruct[
                'noticed_dataProtection'] == u"(u'yes',)" else 'Off'),
        ('YesDeclaration',
         'Yes' if appstruct[
                'understood_declaration'] == u"(u'yes',)" else 'Off'),
        ('YesNotification',
         'Yes' if appstruct[
                'consider_joining'] == u"(u'yes',)" else 'Off'),
        ('created3', 1 if appstruct['at_least_three_works'] == u'yes' else 2),
        ('inColSoc', 1 if appstruct['member_of_colsoc'] == u'yes' else 2),
        ]

# generate fdf string

    fdf = forge_fdf("", fields, [], [], [])

# write to file

    my_fdf_filename = "fdf.fdf"
    fdf_file = open(my_fdf_filename, "w")
    # fdf_file.write(fdf.encode('utf8'))
    if DEBUG:  # pragma: no cover
        print("== PDFTK: write fdf")
    fdf_file.write(fdf)
    if DEBUG:  # pragma: no cover
        print("== PDFTK: close fdf file")
    fdf_file.close()

    if DEBUG:  # pragma: no cover
        print("== PDFTK: fill_form & flatten")

        print("running pdftk...")
    pdftk_output = subprocess.call([
            'pdftk',
            'pdftk/declaration-of-intent.pdf',  # input pdf with form fields
            'fill_form', my_fdf_filename,  # fill in values
            'output', 'formoutput.pdf',  # output filename
            'flatten',  # make form read-only
#            'verbose'  # be verbose?
            ])

    if DEBUG:  # pragma: no cover
        print("===== pdftk output ======")
        print(pdftk_output)


#         os.unlink('formoutput.pdf')
#         if DEBUG:  # pragma: no cover
#             print("== PDFTK: success: deleted formoutput.pdf")
#     except OSError, ose:  # pragma: no cover
#         print ose
#         print("== PDFTK: file not found while trying to delete")
#     if DEBUG:  # pragma: no cover
#         print("== PDFTK: delete fdf with user data: " + my_fdf_filename)

#    try:
#        os.unlink(my_fdf_filename)
#        if DEBUG:  # pragma: no cover
#            print("== PDFTK: success: deleted fdf file")
#    except:  # pragma: no cover
#        print("== PDFTK: error while trying to delete fdf file")
    # return a pdf file
    from pyramid.response import Response
    response = Response(content_type='application/pdf')
    response.app_iter = open("formoutput.pdf", "r")
    return response

from c3sintent.gnupg_encrypt import encrypt_with_gnupg


def accountant_mail(appstruct):

    unencrypted = u"""
Yay!
we got a declaration of intent through the form: \n
name:         \t\t %s
email:        \t\t %s
streetNo:     \t\t %s
address2:     \t\t %s
postCodeCity: \t\t %s
country:      \t\t %s

activities:   \t\t %s
created3:     \t\t $s
member of collecting society:  %s

understood declaration text:  %s
consider joining     \t %s
noticed data protection: \t %s

that's it.. bye!""" % (
        unicode(appstruct['name']),
        unicode(appstruct['email']),
        unicode(appstruct['address1']),
        unicode(appstruct['address2']),
        unicode(appstruct['postCodeCity']),
        unicode(appstruct['country']),
        unicode(appstruct['at_least_three_works']),
        unicode(appstruct['member_of_colsoc']),
        unicode(appstruct['understood_declaration'][0]),
        unicode(appstruct['consider_joining']),
        unicode(appstruct['noticed_dataProtection']),
        )

    message = Message(
        subject="[c3s] Yes! a new letter of intent",
        sender="noreply@c3s.cc",
        recipients=["c@c3s.cc"],
        body=str(encrypt_with_gnupg((unencrypted)))
        )

    attachment = Attachment("foo.gpg", "application/gpg-encryption",
                            unicode(encrypt_with_gnupg(u"foo to the bär!")))
    # TODO: make attachment contents a .csv with the data supplied.
    message.attach(attachment)

    return message
