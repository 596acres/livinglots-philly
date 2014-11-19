# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('steward', '0001_initial'),
        ('livinglots_organize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stewardnotification',
            name='type',
            field=models.ForeignKey(help_text='The type of group working on the project.', to='livinglots_organize.OrganizerType'),
            preserve_default=True,
        ),
    ]
