# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
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
        migrations.AlterField(
            model_name='usersignup',
            name='scope',
            field=models.ForeignKey(to='signup.SignupScope'),
        ),
    ]
