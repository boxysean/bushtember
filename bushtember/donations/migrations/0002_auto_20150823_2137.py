# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_customer_name'),
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadphototoken',
            name='charge',
            field=models.ForeignKey(default=0, to='payments.Charge'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadphototoken',
            name='customer',
            field=models.ForeignKey(default=0, to='payments.Customer'),
            preserve_default=False,
        ),
    ]
