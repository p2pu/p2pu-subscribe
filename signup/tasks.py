from __future__ import absolute_import

from celery import shared_task
from signup import emails


@shared_task
def send_welcome_email(signup):
    emails.send_welcome_email(signup)
