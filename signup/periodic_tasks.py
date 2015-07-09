from __future__ import absolute_import

from celery import shared_task
from signup import emails
from signup.models import get_previous_week_signups
from signup.db import SignupScope


#@shared_task
def send_weekly_digest():
    for scope in SignupScope.objects.all():
        signups = get_previous_week_signups(scope.scope_name)
        # send email to admin user
        # TODO store per scope contact
        # TODO give scope option for weekly digest
        if len(signups) > 0:
            emails.send_weekly_signup_digest(scope.scope_name, signups)
