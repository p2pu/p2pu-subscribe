from django.utils import timezone

import json
import random
import string
import datetime

from signup import db
from signup.tasks import send_welcome_email


def create_signup_scope(scope_name, send_welcome_email, confirm_email, email_subject, email_text, email_html):
    # Check if send_welcome_email is true and if we hae an email template supplied
    email_template = None
    
    if send_welcome_email:
        email_template = db.EmailTemplate()
        if email_subject:
            email_template.subject = email_subject
        # TODO load default template 
        if email_text:
            email_template.text_body = email_text
        if email_html:
            email_template.html_body = email_html
        email_template.save()

    scope_db = db.SignupScope(
        scope_name = scope_name,
        send_welcome_email = send_welcome_email,
        confirm_email = confirm_email,
        email_template = email_template
    )
    scope_db.save()


def _signup2json( signup_db ):
    signup = {
        'email': signup_db.email,
        'scope': signup_db.scope.scope_name,
        'questions': json.loads(signup_db.questions),
        'created_at': signup_db.created_at,
        'updated_at': signup_db.updated_at,
        'deleted_at': signup_db.deleted_at,
    }
    return signup


def create_signup( email, scope_name, questions ):
    """ Add signup to scope """
    scope = db.SignupScope.objects.get(scope_name=scope_name)
    if db.UserSignup.objects.filter(email__iexact=email, scope=scope).exists():
        raise Exception('Signup already exists')
    signup = db.UserSignup(
        email=email,
        scope=scope,
        questions=json.dumps(questions),
    )
    signup.save()
    signup_dict = _signup2json(signup)
    if scope.send_welcome_email:
        send_welcome_email.delay(signup_dict)
    return signup_dict


def update_signup( email, scope, questions ):
    """ Update the signup if it exists for the current scope. If the signup was previously deleted it will be undeleted """
    signup_db = db.UserSignup.objects.get(email__iexact=email, scope__scope_name=scope)

    old_questions = json.loads(signup_db.questions)
    for key, value in questions.items():
        old_questions[key] = value

    signup_db.questions = json.dumps(old_questions)
    signup_db.deleted_at = None
    signup_db.save()
    return _signup2json(signup_db)


def create_or_update_signup( email, scope, questions ):
    # check if user is already added to the scope
    if db.UserSignup.objects.filter(email__iexact=email, scope__scope_name=scope).exists():
        return update_signup(email, scope, questions)
    else:
        return create_signup(email, scope, questions)


def delete_signup( email, scope ):
    if db.UserSignup.objects.filter(email__iexact=email, scope__scope_name=scope, deleted_at__isnull=False).exists():
        raise Exception('Signup already deleted')
    signup_db = db.UserSignup.objects.get(email__iexact=email, scope__scope_name=scope)
    signup_db.deleted_at = timezone.now()
    signup_db.save()
    

def get_signup( email, scope ):
    if not db.UserSignup.objects.filter(email__iexact=email, scope__scope_name=scope, deleted_at__isnull=True).exists():
        raise Exception(u'Signup for {0} not found'.format(email))

    signup_db = db.UserSignup.objects.get(email__iexact=email, scope__scope_name=scope, deleted_at__isnull=True)
    return _signup2json(signup_db)


def get_signups( scope ):
    signups = db.UserSignup.objects.filter(deleted_at__isnull=True, scope__scope_name=scope)
    return [_signup2json(signup) for signup in signups]


def get_previous_week_signups(scope):
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - datetime.timedelta(days=today.weekday()+7)
    signups_db = db.UserSignup.objects.filter(created_at__gte=week_start, created_at__lt=week_start + datetime.timedelta(days=7), scope__scope_name=scope)
    return [ _signup2json(signup) for signup in signups_db ]
