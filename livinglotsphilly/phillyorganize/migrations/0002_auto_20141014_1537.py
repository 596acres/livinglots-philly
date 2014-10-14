# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phillyorganize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='email',
            field=models.EmailField(max_length=75, null=True, verbose_name='email', blank=True),
        ),
    ]
