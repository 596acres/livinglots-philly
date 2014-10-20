# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('forms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyFieldEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_id', models.IntegerField()),
                ('value', models.CharField(max_length=2000, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Form field entry',
                'verbose_name_plural': 'Form field entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyFormEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_time', models.DateTimeField(verbose_name='Date/time')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('survey_form', models.ForeignKey(related_name=b'survey_entries', to='forms.Form')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Form entry',
                'verbose_name_plural': 'Form entries',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='surveyfieldentry',
            name='entry',
            field=models.ForeignKey(related_name=b'fields', to='survey.SurveyFormEntry'),
            preserve_default=True,
        ),
    ]
