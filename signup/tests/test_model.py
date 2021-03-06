from django.test import TestCase
from django.core import mail

from mock import patch
import math
import datetime

from signup import models as signup_models
from signup import randata
from signup.db import SignupScope, EmailTemplate, UserSignup

class ModelTest(TestCase):

    def setUp(self):
        self.signup_data = [
            'dirk@mail.com',
            'test-scope',
            {'q1':'a1', 'q2':'a2', 'q3':'a3'}
        ]
        email_template = EmailTemplate()
        email_template.subject = 'Thanks for signing up'
        email_template.text_body = 'Thanks for signing up'
        email_template.html_body = 'Thanks for signing up'
        email_template.save()

        scope = SignupScope()
        scope.scope_name = 'test-scope'
        scope.send_welcome_email = True
        scope.confirm_email = True
        scope.email_template = email_template
        scope.save()
        scope2 = SignupScope()
        scope2.scope_name = 'test-scope-2'
        scope2.send_welcome_email = False
        scope2.confirm_email = False
        scope2.save()

        self.patch1 = patch('signup.models.send_welcome_email.delay')
        self.send_welcome_email = self.patch1.start()


    def tearDown(self):
        self.patch1.stop()


    def test_create_signup(self):
        """
        Test creation of a signup
        """
        signup_models.create_signup(*self.signup_data)
        signup = signup_models.get_signup('dirk@mail.com', 'test-scope')
        self.assertEqual(signup['email'], 'dirk@mail.com')
        self.assertEqual(signup['questions']['q1'], 'a1')
        self.assertEqual(signup['questions']['q2'], 'a2')
        self.assertEqual(signup['questions']['q3'], 'a3')
        self.assertIn('created_at', signup)
        self.assertIn('updated_at', signup)
        self.assertTrue(self.send_welcome_email.called)


    def test_create_signup_in_nonexistent_scope(self):
        with self.assertRaises(Exception):
            signup_models.create_signup('bob@mail.net', '123456789', {})

        with self.assertRaises(Exception):
            signup = signup_models.get_signup('bob@mail.net', '123456789')


    def test_update_signup(self):
        original = signup_models.create_or_update_signup(*self.signup_data)
        signup_models.create_or_update_signup('dirk@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup = signup_models.get_signup('dirk@mail.com', 'test-scope')
        self.assertEqual(signup['email'], 'dirk@mail.com')
        self.assertEqual(signup['questions']['q1'], 'ar1')
        self.assertEqual(signup['questions']['q2'], 'ar2')
        self.assertEqual(signup['questions']['q3'], 'a3')
        self.assertEqual(original['created_at'], signup['created_at'])
        self.assertNotEqual(original['updated_at'], signup['updated_at'])


    def test_get_signups(self):
        signup_models.create_or_update_signup('user1@mail.com', 'test-scope', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user4@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})

        self.assertEqual(len(signup_models.get_signups('test-scope')), 4)


    def test_get_signups_for_scope(self):
        signup_models.create_or_update_signup('user1@mail.com', 'test-scope', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        
        signup_models.create_or_update_signup('user3@mail.com', 'test-scope-2', {'q1':'ar1'})
        signup_models.create_or_update_signup('user4@mail.com', 'test-scope-2', {'q1':'ar1'})
        signup_models.create_or_update_signup('user5@mail.com', 'test-scope-2', {'q1':'ar1'})
        signup_models.create_or_update_signup('user6@mail.com', 'test-scope-2', {'q1':'ar1'})

        self.assertEqual(len(signup_models.get_signups('test-scope')), 3)
        self.assertEqual(len(signup_models.get_signups('test-scope-2')), 4)


#    def test_handle_new_signups(self, add_list_member, delete_all_unsubscribes):
#        signup_models.create_or_update_signup('user1@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
#        self.assertEqual(len(signup_models.get_new_signups()), 1)
#
#        with patch('signup.models.mailgun_api.send_mass_email') as send_email:
#            signup_models.handle_new_signups()
#            self.assertTrue(send_email.called)
#            self.assertTrue(add_list_member.called)
#            self.assertTrue(delete_all_unsubscribes.called)
#
#        self.assertEqual(len(signup_models.get_new_signups()), 0)


 #   @patch('signup.models.emails.send_welcome_emails')
 #   def test_scale_signups(self, blah, send_email, add_list_member):
 #       for signup in randata.random_data(2000):
 #           signup_models.create_or_update_signup(**signup)
 #
 #       signups = len(signup_models.get_new_signups())
 #
 #           signup_models.handle_new_signups()
 #           self.assertTrue(send_email.called)
 #           self.assertEqual(send_email.call_count, math.ceil(signups/500.0))
 #           self.assertTrue(add_list_member.called)
 #           self.assertEqual(add_list_member.call_count, signups)

 #       self.assertEqual(len(signup_models.get_new_signups()), 0)


    def test_delete_signup(self):
        signup_models.create_or_update_signup('user1@mail.com', 'test-scope', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user4@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})

        self.assertEqual(len(signup_models.get_signups('test-scope')), 4)
        new_signups = signup_models.get_signups('test-scope')
        self.assertIn('user3@mail.com', [s['email'] for s in new_signups])

        signup_models.delete_signup('user3@mail.com', 'test-scope')

        signups = signup_models.get_signups('test-scope')
        self.assertEqual(len(signups), 3)
        self.assertNotIn('user3@mail.com', [s['email'] for s in signups])

        signup_models.create_or_update_signup('user3@mail.com', 'test-scope', {'q1':'ar1', 'q2':'ar2'})
        self.assertEqual(len(signup_models.get_signups('test-scope')), 4)
        signups = signup_models.get_signups('test-scope')
        self.assertIn('user3@mail.com', [s['email'] for s in signups])


    def test_case_insensitve_signup(self):
        signup_models.create_or_update_signup('thisisauser@mail.com', 'test-scope', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup = signup_models.get_signup('ThisIsAUser@mail.COM', 'test-scope')
        self.assertEquals(signup['email'], 'thisisauser@mail.com')

    def test_send_welcome_email(self):
        from signup import emails
        signup = signup_models.create_or_update_signup('thisisauser@mail.com', 'test-scope', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        emails.send_welcome_email(signup)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Thanks for signing up')

    def test_getting_previous_week_signups(self):
        signup_models.create_signup('mail1@mail.com', 'test-scope', {})
        signup_models.create_signup('mail2@mail.com', 'test-scope', {})
        signup_models.create_signup('mail3@mail.com', 'test-scope', {})
        signup_models.create_signup('mail4@mail.com', 'test-scope', {})
        signup_models.create_signup('mail5@mail.com', 'test-scope', {})
        signup_models.create_signup('mail6@mail.com', 'test-scope', {})

        # Change 2 signup to a week ago
        s2 = UserSignup.objects.get(email='mail2@mail.com')
        s2.created_at = s2.created_at - datetime.timedelta(days=7)
        s2.save()
        
        s3 = UserSignup.objects.get(email='mail3@mail.com')
        s3.created_at = s3.created_at - datetime.timedelta(days=7)
        s3.save()

        # Change 1 signup to two weeks ago
        s4 = UserSignup.objects.get(email='mail4@mail.com')
        s4.created_at = s4.created_at - datetime.timedelta(days=14)
        s4.save()

        # Change 1 signup to the start of the week
        s5 = UserSignup.objects.get(email='mail5@mail.com')
        s5.created_at = s5.created_at.replace(hour=0, minute=0, second=0, microsecond=0)
        s5.created_at = s5.created_at - datetime.timedelta(days=s5.created_at.weekday())
        s5.save()

        # Change 1 signup to start of previous week 
        s6 = UserSignup.objects.get(email='mail6@mail.com')
        s6.created_at = s6.created_at.replace(hour=0, minute=0, second=0, microsecond=0)
        s6.created_at = s6.created_at - datetime.timedelta(days=s6.created_at.weekday()+7)
        s6.save()

        # At this point the follow signups should be part of the previous weeks signups:
        # ['mail2@mail.com', 'mail3@mail.com', 'mail6@mail.com']
        emails = [ s['email'] for s in signup_models.get_previous_week_signups('test-scope')]
        for email in['mail2@mail.com', 'mail3@mail.com', 'mail6@mail.com']:
            self.assertIn(email, emails)



