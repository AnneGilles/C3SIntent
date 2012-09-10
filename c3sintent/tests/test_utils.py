# -*- coding: utf-8  -*-
import unittest
from pyramid import testing

from c3sintent.models import DBSession


def _initTestingDB():
    """
    set up a database to run tests against
    """
    from sqlalchemy import create_engine
    from c3sintent.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session


class TestUtilities(unittest.TestCase):
    """
    tests for c3sintent/utils.py
    """
    def setUp(self):
        """
        set up everything for a test case
        """
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')
        DBSession.remove()
        self.session = _initTestingDB()

    def tearDown(self):
        """
        clean up after a test case
        """
        DBSession.remove()
        testing.tearDown()

    def test_generate_pdf_en(self):
        """
        Test pdf generation
        and resulting pdf size
        """
        from c3sintent.views import generate_pdf

        mock_appstruct = {
            'firstname': u'Anne',
            'lastname': u'Gilles',
            'address1': u'Sonnenstraße 23',
            'address2': u'12345 Müsterstädt',
            'postCode': '12345',
            'city': 'City',
            'email': u'foo@example.com',
            'country': 'country',
            'activity': set([u'composer', u'lyricist', u'dj']),
            'at_least_three_works': 'at_least_three_works',
            'member_of_colsoc': 'member_of_colsoc',
            'understood_declaration': 'understood_declaration',
            'consider_joining': 'consider_joining',
            'noticed_dataProtection': 'noticed_dataProtection',
            '_LOCALE_': 'en',
            }

        # a skipTest iff pdftk is not installed
        import subprocess
        from subprocess import CalledProcessError
        try:
            res = subprocess.check_call(
                ["which", "pdftk"], stdout=None)
            if res == 0:
                # go ahead with the tests
                result = generate_pdf(mock_appstruct)

                self.assertEquals(result.content_type,
                                  'application/pdf')
                #print("size of pdf: " + str(len(result.body)))
                # check pdf size
                self.assertTrue(100000 > len(result.body) > 78000)

                # TODO: check pdf for contents

        except CalledProcessError, cpe:  # pragma: no cover
            print("pdftk not installed. skipping test!")
            print(cpe)

    def test_generate_pdf_de(self):
        """
        Test pdf generation
        and resulting pdf size
        """
        from c3sintent.views import generate_pdf

        mock_appstruct = {
            'firstname': u'Anne',
            'lastname': u'Gilles',
            'address1': u'Sonnenstraße 23',
            'address2': u'12345 Müsterstädt',
            'postCode': '12345',
            'city': 'City',
            'email': u'foo@example.com',
            'country': 'country',
            'activity': set([u'composer', u'lyricist', u'dj']),
            'at_least_three_works': 'at_least_three_works',
            'member_of_colsoc': 'member_of_colsoc',
            'understood_declaration': 'understood_declaration',
            'consider_joining': 'consider_joining',
            'noticed_dataProtection': 'noticed_dataProtection',
            '_LOCALE_': 'de',
            }

        # a skipTest iff pdftk is not installed
        import subprocess
        from subprocess import CalledProcessError
        try:
            res = subprocess.check_call(
                ["which", "pdftk"], stdout=None)
            if res == 0:
                # go ahead with the tests
                result = generate_pdf(mock_appstruct)

                self.assertEquals(result.content_type,
                                  'application/pdf')
                #print("size of pdf: " + str(len(result.body)))
                # check pdf size
                self.assertTrue(100000 > len(result.body) > 78000)

                # TODO: check pdf for contents

        except CalledProcessError, cpe:  # pragma: no cover
            print("pdftk not installed. skipping test!")
            print(cpe)

    def test_generate_csv(self):
        """
        test creation of csv snippet
        """
        from c3sintent.utils import generate_csv
        my_appstruct = {
            'activity': ['composer', 'dj'],
            'firstname': 'John',
            'lastname': 'Doe',
            'address1': 'In the Middle',
            'address2': 'Of Nowhere',
            'postCode': '12345',
            'city': 'Town',
            'email': 'john@example.com',
            'country': 'de',
            'at_least_three_works': 'yes',
            'member_of_colsoc': 'yes',
            'understood_declaration': 'yes',
            'consider_joining': 'yes',
            'noticed_dataProtection': 'yes'
            }
        result = generate_csv(my_appstruct)
        #print(result)
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        #print(today)
        self.failUnless(
            result == str(today + ';unknown;pending...;John;Doe;' +
                          'john@example.com;In the Middle;Of Nowhere;' +
                          '12345;Town;de;j;n;n;n;n;j;j;j;j;j;j'))

    def test_accountant_mail(self):
        """
        test encryption of email payload
        """
        from c3sintent.utils import accountant_mail
        my_appstruct = {
            'activity': ['composer', 'dj'],
            'firstname': 'John',
            'lastname': 'Doe',
            'address1': 'In the Middle',
            'address2': 'Of Nowhere',
            'postCode': '12345',
            'city': 'Town',
            'email': 'john@example.com',
            'country': 'af',
            'at_least_three_works': 'yes',
            'member_of_colsoc': 'yes',
            'understood_declaration': 'yes',
            'consider_joining': 'yes',
            'noticed_dataProtection': 'yes'
            }
        result = accountant_mail(my_appstruct)
        from pyramid_mailer.message import Message

        self.assertTrue(isinstance(result, Message))
        self.assertTrue('c@c3s.cc' in result.recipients)
        self.assertTrue('-----BEGIN PGP MESSAGE-----' in result.body)
        self.assertTrue('-----END PGP MESSAGE-----' in result.body)
        self.assertTrue('[c3s] Yes! a new letter of intent' in result.subject)
        self.assertEquals('noreply@c3s.cc', result.sender)
