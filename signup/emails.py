from django.conf import settings
from django.template.loader import render_to_string
from django.core.email import send_mail

def send_welcome_emails(emails):
    subject = render_to_string('signup/emails/signup-confirmation-subject.txt', {}).strip()
    text_body = render_to_string('signup/emails/signup-confirmation.txt', {}).strip()
    html_body = render_to_string('signup/emails/signup-confirmation.html', {}).strip()
    send_mail(
        subject,
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        emails,
        fail_silently=False,
        html_message=html_body
    )
