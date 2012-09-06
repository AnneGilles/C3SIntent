#!/bin/env/python
# -*- coding: utf-8 -*-
# http://docs.pylonsproject.org/projects/pyramid/dev/narr/testing.html
#                                            #creating-functional-tests
import unittest


class FunctionalTests(unittest.TestCase):
    """
    this test is a functional test to check functionality of the whole app

    it also serves to get coverage for 'main'
    """
    def setUp(self):
        my_settings = {'sqlalchemy.url': 'sqlite://'}  # mock, not even used!?
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

    def test_z_root(self):
        """load the front page, check string exists"""
        res = self.testapp.get('/', status=200)
        self.failUnless('Cultural Commons Collecting Society' in res.body)

    def test_lang_en(self):
        """load the front page, check english string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/?_LOCALE_=en', status=200)
        self.failUnless('When we' in res.body)

#     def test_lang_de(self):
#         """load the front page, check german string exists"""
#         res = self.testapp.get('/?_LOCALE_=de', status=200)
#         self.failUnless('Willkommen bei der OpenMusicContest.org' in res.body)

#     def test_no_cookies(self):
#         """load the front page, check default english string exists"""
#         res = self.testapp.reset()
#         res = self.testapp.get('/', status=200,
#                                headers={
#                 'Accept-Language': 'da,en-gb; q=0.8, en; q=0.7'})
#        self.failUnless('Welcome to the OpenMusicContest.org' in res.body)

    def test_form_lang_en(self):
        """load the join form, check english string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/?_LOCALE_=en', status=200)
        self.failUnless('Please answer all questions' in res.body)

    def test_form_lang_en_non_validating(self):
        """load the join form, check english string exists"""
        res = self.testapp.reset()
        res = self.testapp.get('/?_LOCALE_=en', status=200)

        form = res.form
        print(form.fields)
        #print(form.fields.values())
        form['name'] = 'John Doe'
        form['address2'] = 'some address part'
        res2 = form.submit('submit')
        self.failUnless(
            'There was a problem with your submission' in res2.body)

    def test_form_lang_de(self):
        """load the join form, check german string exists"""
        res = self.testapp.get('/?_LOCALE_=de', status=200)
        self.failUnless('Bitte fülle das Formular aus' in res.body)
