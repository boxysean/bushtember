# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import donations.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_customer_name'),
        ('donations', '0004_auto_20150826_0412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(default=donations.models.generate_token, max_length=36)),
                ('uploaded_image', models.CharField(max_length=255, null=True, blank=True)),
                ('uploaded_image_approved', models.NullBooleanField()),
                ('modified_image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('modified_image_approved', models.NullBooleanField()),
                ('collage_image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('charge', models.ForeignKey(to='payments.Charge')),
                ('customer', models.ForeignKey(to='payments.Customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='uploadphototoken',
            name='charge',
        ),
        migrations.RemoveField(
            model_name='uploadphototoken',
            name='customer',
        ),
        migrations.DeleteModel(
            name='UploadPhotoToken',
        ),
    ]
