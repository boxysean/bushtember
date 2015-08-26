# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_uploadphototoken_image_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadphototoken',
            name='image_path',
        ),
        migrations.AddField(
            model_name='uploadphototoken',
            name='collage_image',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='uploadphototoken',
            name='modified_image',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='uploadphototoken',
            name='modified_image_approved',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='uploadphototoken',
            name='uploaded_image',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='uploadphototoken',
            name='uploaded_image_approved',
            field=models.NullBooleanField(),
        ),
    ]
