# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('violations', '0003_auto_20141015_1947'),
        ('pathways', '0002_auto_20141222_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathway',
            name='violation_types',
            field=models.ManyToManyField(help_text='This pathway applies to lots with these violation types.', to='violations.ViolationType', null=True, blank=True),
            preserve_default=True,
        ),
    ]
