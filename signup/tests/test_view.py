"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from mock import patch
import math

from signup import models as signup_models
from signup import randata
from signup.db import SignupScope

class ViewTest(TestCase):

    SIGNUP_DATA = {
        'email': 'dirk@mail.com',
        'scope': 'test-scope',
        'timezone': 'Africa/Johannesburg',
        'groupRadios': 'true', 
        'styleRadios': 'try', 
        'expertiseRadios': 'think',
        'csrfmiddlewaretoken': '123'
    }

    def setUp(self):
        scope = SignupScope()
        scope.scope_name = 'test-scope'
        scope.send_welcome_email = True
        scope.confirm_email = True
        scope.save()


    def test_signup_view(self):
        c = Client()
        resp = c.post('/signup/', self.SIGNUP_DATA)
        self.assertRedirects(resp, '/success/')


    def test_signup_api(self):
        c = Client()
        api_data = {
            'email': 'test@mail.com',
            'scope': 'test-scope',
            'locations': ['location1', 'location2'],
        }
        resp = c.post('/api/signup/', api_data)
        self.assertEqual(resp.status_code, 200)


    def test_wrong_scope(self):
        c = Client()
        api_data = {
            'email': 'test@mail.com',
            'scope': 'test-non-existant-scope',
            'locations': ['location1', 'location2'],
        }
        resp = c.post('/api/signup/', api_data)
        self.assertEqual(resp.status_code, 400)

