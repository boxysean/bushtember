# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import donations.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_auto_20150830_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='collage_image',
            field=models.ImageField(null=True, upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='modified_image',
            field=models.ImageField(null=True, upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='token',
            field=models.CharField(default=donations.models.generate_token, max_length=36, db_index=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='uploaded_image',
            field=models.ImageField(null=True, upload_to=b'uploads', blank=True),
        ),
    ]
