from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template import Template
from django.template import Context

from signup.db import SignupScope

def send_welcome_email(signup):
    scope = SignupScope.objects.get(scope_name=signup['scope'])
    if scope.email_template == None:
        raise Exception("Cannot send an confirmation email without a template")
    subject = Template(scope.email_template.subject).render(Context({})).strip()
    text_body = Template(scope.email_template.text_body).render(Context({})).strip()
    html_body = Template(scope.email_template.html_body).render(Context({})).strip()
    send_mail(
        subject,
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        [signup['email']],
        fail_silently=False,
        html_message=html_body
    )
