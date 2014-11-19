# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phillyorganize', '0002_auto_20141014_1537'),
        ('livinglots_organize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='type',
            field=models.ForeignKey(to='livinglots_organize.OrganizerType'),
            preserve_default=True,
        ),
    ]
