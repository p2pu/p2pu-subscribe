# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.TextField()),
                ('text_body', models.TextField()),
                ('html_body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SignupScope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scope_name', models.CharField(unique=True, max_length=256)),
                ('send_welcome_email', models.BooleanField()),
                ('confirm_email', models.BooleanField()),
                ('email_template', models.ForeignKey(blank=True, to='signup.EmailTemplate', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('questions', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('confirmed_at', models.DateTimeField(null=True, blank=True)),
                ('scope', models.ForeignKey(to='signup.SignupScope')),
            ],
        ),
    ]
