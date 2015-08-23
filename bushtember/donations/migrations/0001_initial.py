# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import donations.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadPhotoToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(default=donations.models.generate_token, max_length=36)),
                ('customer', models.ForeignKey(to='payments.Customer', null=True)),
            ],
        ),
    ]
