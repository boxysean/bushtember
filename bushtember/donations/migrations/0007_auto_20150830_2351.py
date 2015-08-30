# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_auto_20150830_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='collage_image',
            field=models.ImageField(null=True, upload_to=b'/Users/boxysean/workspace/bushtember/bushtember/../www/media/uploads/', blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='modified_image',
            field=models.ImageField(null=True, upload_to=b'/Users/boxysean/workspace/bushtember/bushtember/../www/media/uploads/', blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='uploaded_image',
            field=models.ImageField(null=True, upload_to=b'/Users/boxysean/workspace/bushtember/bushtember/../www/media/uploads/', blank=True),
        ),
    ]
