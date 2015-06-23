from django.utils import timezone

import json
import random
import string

from signup import db
#from signup import emails


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
    if scope.send_welcome_email:
        # TODO Send welcome email
        pass
    return _signup2json(signup)


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


#   def get_new_signups( ):
#       """ get signups where the welcome email hasn't been sent yet """
#       signups = db.UserSignup.objects.filter(tasks_handled_at__isnull=True, deleted_at__isnull=True)
#       return [_signup2json(signup) for signup in signups]


#   def handle_new_signups( ):
#       """ Send welcome email to new users.
#           Add them to a general mailing list. 
#           Update db when done. """
#       signups = db.UserSignup.objects.filter(tasks_handled_at__isnull=True, deleted_at__isnull=True)[:500]
#       while len(signups):
#           emails.send_welcome_emails([signup.email for signup in signups])
#           db.UserSignup.objects.filter(id__in=signups.values('id')).update(tasks_handled_at=timezone.now())
#           signups = db.UserSignup.objects.filter(tasks_handled_at__isnull=True, deleted_at__isnull=True)[:500]
