from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField()
    scope = forms.CharField(max_length=1024)
