from django.db import models


class UserSignup(models.Model):
    email = models.EmailField()
    scope = models.CharField(max_length=1024)
    questions = models.TextField() # Questions and answers stored as a JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
