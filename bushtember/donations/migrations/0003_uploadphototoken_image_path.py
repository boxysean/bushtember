# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_auto_20150823_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadphototoken',
            name='image_path',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
