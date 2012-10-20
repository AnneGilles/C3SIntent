#!/bin/env/python
# -*- coding: utf-8 -*-
# http://docs.pylonsproject.org/projects/pyramid/dev/narr/testing.html
#                                            #creating-functional-tests
import unittest


class FunctionalTests(unittest.TestCase):
    """
    these tests are functional tests to check functionality of the whole app

    they also serve to get coverage for 'main'
    """
    def setUp(self):
        my_settings = {'sqlalchemy.url': 'sqlite://',
                       'available_languages': 'da de en es fr'}
                        # mock, not even used!?
        #from sqlalchemy import engine_from_config
        #engine = engine_from_config(my_settings)

        from c3sintent import main
        app = main({}, **my_settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        # maybe I need to check and remove globals here,
        # so the other tests are not compromised
        #del engine
        from c3sintent.models import DBSession
        DBSession.remove()

    def test_base_template(self):
        """load the front page, check string exists"""
        res = self.testapp.get('/', status=200)
        self.failUnless('Cultural Commons Collecting Society' in res.body)
        self.failUnless(
            'Copyright 2012, OpenMusicContest.org e.V.' in res.body)

    def test_lang_en_LOCALE(self):
        """load the front page, forced to english (default pyramid way),
        check english string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/?_LOCALE_=en', status=200)
        self.failUnless('When we' in res.body)

    def test_lang_en(self):
        """load the front page, set to english (w/ pretty query string),
        check english string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/?en', status=302)
        self.failUnless('The resource was found at' in res.body)
        # we are being redirected...
        res1 = res.follow()
        self.failUnless('When we' in res1.body)

# so let's test the app's obedience to the language requested by the browser
# i.e. will it respond to http header Accept-Language?

    def test_accept_language_header_da(self):
        """check the http 'Accept-Language' header obedience: danish
        load the front page, check danish string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/', status=200,
                               headers={
                'Accept-Language': 'da'})
        #print(res.body) #  if you want to see the pages source
        self.failUnless(
            '<input type="hidden" name="_LOCALE_" value="da"' in res.body)

    def test_accept_language_header_de_DE(self):
        """check the http 'Accept-Language' header obedience: german
        load the front page, check german string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/', status=200,
                               headers={
                'Accept-Language': 'de-DE'})
        #print(res.body) #  if you want to see the pages source
        self.failUnless(
            'zum geplanten Beitritt' in res.body)
        self.failUnless(
            '<input type="hidden" name="_LOCALE_" value="de"' in res.body)

    def test_accept_language_header_en(self):
        """check the http 'Accept-Language' header obedience: english
        load the front page, check english string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/', status=200,
                               headers={
                'Accept-Language': 'en'})
        #print(res.body) #  if you want to see the pages source
        self.failUnless(
            'You have to be a composer, lyricist, musician, music producer, '
            + 'remixer or DJ' in res.body)

    def test_accept_language_header_es(self):
        """check the http 'Accept-Language' header obedience: spanish
        load the front page, check spanish string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/', status=200,
                               headers={
                'Accept-Language': 'es'})
        #print(res.body) #  if you want to see the pages source
        self.failUnless(
            'Luego de enviar el siguiente formulario,' in res.body)

    def test_accept_language_header_fr(self):
        """check the http 'Accept-Language' header obedience: french
        load the front page, check french string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/', status=200,
                               headers={
                'Accept-Language': 'fr'})
        #print(res.body) #  if you want to see the pages source
        self.failUnless(
            'En envoyant un courriel à data@c3s.cc vous pouvez' in res.body)

    def test_no_cookies(self):
        """load the front page, check default english string exists"""
        res = self.testapp.reset()  # delete cookie
        res = self.testapp.get('/', status=200,
                               headers={
                'Accept-Language': 'af, cn'})  # ask for missing languages
        #print res.body
        self.failUnless('Declaration' in res.body)

#############################################################################
# check for validation stuff

    def test_form_lang_en_non_validating(self):
        """load the join form, check english string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/?_LOCALE_=en', status=200)
        form = res.form
        #print(form.fields)
        #print(form.fields.values())
        form['firstname'] = 'John'
        form['address2'] = 'some address part'
        res2 = form.submit('submit')
        self.failUnless(
            'There was a problem with your submission' in res2.body)

    def test_form_lang_de(self):
        """load the join form, check german string exists"""
        res = self.testapp.get('/?de', status=302)
        #print(res)
        self.failUnless('The resource was found at' in res.body)
        # we are being redirected...
        res2 = res.follow()
        # test for german translation of template text (lingua_xml)
        self.failUnless('Bei Antragstellung zur Zulassung als' in res2.body)
        # test for german translation of form field label (lingua_python)
        self.failUnless('Texter' in res2.body)

    def test_form_lang_LOCALE_de(self):
        """load the join form in german, check german string exists
        this time forcing german locale the pyramid way
        """
        res = self.testapp.get('/?_LOCALE_=de', status=200)
        # test for german translation of template text (lingua_xml)
        self.failUnless('Bei Antragstellung zur Zulassung als' in res.body)
        # test for german translation of form field label (lingua_python)
        self.failUnless('Texter' in res.body)

###########################################################################
# checking the disclaimer

    def test_disclaimer_en(self):
        """load the disclaimer in english (via query_string),
        check english string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/disclaimer?en', status=302)
        self.failUnless('The resource was found at' in res.body)
        # we are being redirected...
        res1 = res.follow()
        self.failUnless(
            'you may order your data to be deleted at any time' in str(
                res1.body),
            'expected string was not found in web UI')

    def test_disclaimer_de(self):
        """load the disclaimer in german (via query_string),
        check german string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/disclaimer?de', status=302)
        self.failUnless('The resource was found at' in res.body)
        # we are being redirected...
        res1 = res.follow()
        self.failUnless(
            'Die mit der Absichtserklärung zum geplanten Beitritt der' in str(
                res1.body),
            'expected string was not found in web UI')

    def test_disclaimer_LOCALE_en(self):
        """load the disclaimer in english, check english string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/disclaimer?_LOCALE_=en', status=200)
        self.failUnless(
            'you may order your data to be deleted at any time' in str(
                res.body),
            'expected string was not found in web UI')

    def test_disclaimer_LOCALE_de(self):
        """load the disclaimer in german, check german string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/disclaimer?_LOCALE_=de', status=200)
        self.failUnless(
            'Die mit der Absichtserklärung zum geplanten Beitritt der' in str(
                res.body),
            'expected string was not found in web UI')
