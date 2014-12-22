# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0001_initial'),
        ('pathways', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathway',
            name='specific_private_owners',
            field=models.ManyToManyField(help_text='This pathway applies to lots with these private owners.', related_name='private+', null=True, to='owners.Owner', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pathway',
            name='private_owners',
            field=models.BooleanField(default=False, help_text='This pathway applies to lots with private owners.', verbose_name='private owners'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pathway',
            name='public_owners',
            field=models.BooleanField(default=False, help_text='This pathway applies to lots with public owners.', verbose_name='public owners'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pathway',
            name='specific_public_owners',
            field=models.ManyToManyField(help_text='This pathway applies to lots with these public owners.', related_name='public+', null=True, to='owners.Owner', blank=True),
            preserve_default=True,
        ),
    ]
