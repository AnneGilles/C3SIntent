# -*- coding: utf-8  -*-
import os
import subprocess
from fdfgen import forge_fdf
from c3sintent.gnupg_encrypt import encrypt_with_gnupg
from pyramid_mailer.message import Message
from pyramid_mailer.message import Attachment

DEBUG = False


def generate_pdf(appstruct):
    """
    this function receives an appstruct
    (a datastructure received via formsubmission)
    and prepares and returns a PDF using pdftk
    """
    DEBUG = False

    my_fdf_filename = "custom.fdf"
    my_pdf_filename = "custom.pdf"

    declaration_pdf_de = "pdftk/absichtserklaerung.pdf"
    declaration_pdf_en = "pdftk/declaration-of-intent.pdf"

# check for _LOCALE_, decide which language to use
    #print(appstruct['_LOCALE_'])
    if appstruct['_LOCALE_'] == "de":
        pdf_to_be_used = declaration_pdf_de
    elif appstruct['_LOCALE_'] == "en":
        pdf_to_be_used = declaration_pdf_en
    else:  # pragma: no cover
        # default fallback: english
        pdf_to_be_used = declaration_pdf_en

# here we gather all information from the supplied data to prepare pdf-filling

    fields = [
        ('FirstName', appstruct['firstname']),
        ('LastName', appstruct['lastname']),
        ('streetNo', appstruct['address1']),
        ('address2', appstruct['address2']),
        ('postCode', appstruct['postCode']),
        ('city', appstruct['city']),
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

# write it to a file

    fdf_file = open(my_fdf_filename, "w")

    if DEBUG:  # pragma: no cover
        print("== PDFTK: write fdf")

    fdf_file.write(fdf)

    if DEBUG:  # pragma: no cover
        print("== PDFTK: close fdf file")
    fdf_file.close()

# process the PDF, fill in prepared data

    if DEBUG:  # pragma: no cover
        print("== PDFTK: fill_form & flatten")

        print("running pdftk...")
    pdftk_output = subprocess.call([
            'pdftk',
            pdf_to_be_used,  # input pdf with form fields
            'fill_form', my_fdf_filename,  # fill in values
            'output', my_pdf_filename,  # output filename
            'flatten',  # make form read-only
#            'verbose'  # be verbose?
            ])

    if DEBUG:  # pragma: no cover
        print("===== pdftk output ======")
        print(pdftk_output)

# return a pdf file
    from pyramid.response import Response
    response = Response(content_type='application/pdf')
    response.app_iter = open(my_pdf_filename, "r")

# remove the customized fdf and pdf
    try:
        os.unlink(my_fdf_filename)
        os.unlink(my_pdf_filename)
    except:  # pragma: no cover
        print('error while unlinking pdf or fdf')
        pass

    return response


def generate_csv(appstruct):
    """
    returns a csv with the relevant data
    to ease import of new data sets
    """
    from datetime import date
    import tempfile
    # format:
    # date; place; signature; firstname; lastname; email; streetNo; address2;
    # postCode; city; country; composer; lyricist; musician; producer; remixer;
    # dj; 3works; member_colsoc; read_all; contact; dataProtection

    csv = tempfile.TemporaryFile()
    csv.write(
        (u"%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") % (
            date.today().strftime("%Y-%m-%d"),  # date, e.g. 2012-09-02
            'unknown',  # #                           # place of signature
            'pending...',  # #                           # has signature
            unicode(appstruct['firstname']),  # #    # lastname
            unicode(appstruct['lastname']),  # #    # surname
            unicode(appstruct['email']),  # #   # email
            unicode(appstruct['address1']),  # ## street & no
            unicode(appstruct['address2']),  # ## address cont'd
            unicode(appstruct['postCode']),
            unicode(appstruct['city']),
            unicode(appstruct['country']),  # # # country
            'j' if 'composer' in appstruct['activity'] else 'n',
            'j' if 'lyricist' in appstruct['activity'] else 'n',
            'j' if 'musician' in appstruct['activity'] else 'n',
            'j' if 'producer' in appstruct['activity'] else 'n',
            'j' if 'remixer' in appstruct['activity'] else 'n',
            'j' if 'dj' in appstruct['activity'] else 'n',
            'j' if appstruct['at_least_three_works'] == 'yes'  else 'n',
            'j' if appstruct['member_of_colsoc'] == 'yes'  else 'n',
            'j' if appstruct['understood_declaration'] == 'yes'  else 'n',
            'j' if appstruct['consider_joining'] == 'yes'  else 'n',
            'j' if appstruct['noticed_dataProtection'] == 'yes'  else 'n',
            ))
    # print for debugging? seek to beginning!
    #csv.seek(0)
    #print str(csv.read())
    csv.seek(0)
    return str(csv.read())


def accountant_mail(appstruct):
    unencrypted = u"""
Yay!
we got a declaration of intent through the form: \n
firstname:    \t\t %s
lastname:     \t\t %s
email:        \t\t %s
street & no:  \t\t %s
address2:     \t\t %s
postcode:     \t\t %s
city:         \t\t %s
country:      \t\t %s

activities:   \t\t %s
created3:     \t\t $s
member of collecting society:  %s

understood declaration text:  %s
consider joining     \t %s
noticed data protection: \t %s

that's it.. bye!""" % (
        unicode(appstruct['firstname']),
        unicode(appstruct['lastname']),
        unicode(appstruct['email']),
        unicode(appstruct['address1']),
        unicode(appstruct['address2']),
        unicode(appstruct['postCode']),
        unicode(appstruct['city']),
        unicode(appstruct['country']),
        unicode(appstruct['at_least_three_works']),
        unicode(appstruct['member_of_colsoc']),
        unicode(appstruct['understood_declaration']),
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
                            unicode(encrypt_with_gnupg(u"foo to the bar!")))
    # TODO: make attachment contents a .csv with the data supplied.
    message.attach(attachment)

    return message
