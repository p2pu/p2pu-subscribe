from django.db import models

class EmailTemplate(models.Model):
    subject = models.TextField()
    text_body = models.TextField()
    html_body = models.TextField()


class SignupScope(models.Model):
    scope_name = models.CharField(max_length=256, unique=True)
    send_welcome_email = models.BooleanField()
    confirm_email = models.BooleanField()
    email_template = models.ForeignKey(EmailTemplate, null=True, blank=True)


class UserSignup(models.Model):
    email = models.EmailField()
    scope = models.ForeignKey(SignupScope)
    questions = models.TextField() # Questions and answers stored as a JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
