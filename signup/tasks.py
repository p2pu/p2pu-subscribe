from __future__ import absolute_import

from celery import shared_task
from signup import emails

@shared_task
def send_welcome_email(signup):
    emails.send_welcome_email(signup)


def send_weekly_digest():
    # TODO do this for all scopes
    pass
    #signups = get_previous_week_signups()
    # send email to admin user
