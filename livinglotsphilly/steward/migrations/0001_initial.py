# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phillyorganize', '0002_auto_20141014_1537'),
        ('organize', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptedInStewardProjectManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StewardNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(help_text='The name of the project using this lot.', max_length=256, verbose_name='name')),
                ('support_organization', models.CharField(help_text="What is your project's support organization, if any?", max_length=300, null=True, verbose_name='support organization', blank=True)),
                ('land_tenure_status', models.CharField(default='not sure', help_text='What is the land tenure status for the project? (This will not be shared publicly.)', max_length=50, verbose_name='land tenure status', choices=[(b'owned', 'project owns the land'), (b'licensed', 'project has a license for the land'), (b'lease', 'project has a lease for the land'), (b'access', 'project has access to the land'), (b'not sure', "I'm not sure")])),
                ('include_on_map', models.BooleanField(default=False, help_text='Can we include the project on our map?', verbose_name='include on map')),
                ('phone', models.CharField(help_text='A phone number where the project can be reached.', max_length=32, null=True, verbose_name='phone', blank=True)),
                ('email', models.EmailField(help_text='An email address where the project can be reached.', max_length=75, verbose_name='email')),
                ('url', models.URLField(help_text='A website where others can learn more about the project.', null=True, verbose_name='url', blank=True)),
                ('facebook_page', models.CharField(help_text=b'The Facebook page for the project. Please do not enter your personal Facebook page.', max_length=256, null=True, verbose_name='facebook page', blank=True)),
                ('share_contact_details', models.BooleanField(default=False, help_text="Can we share your contact information (email and phone) on the project's page?", verbose_name='share contact details')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('type', models.ForeignKey(help_text='The type of group working on the project.', to='organize.OrganizerType')),
                ('use', models.ForeignKey(verbose_name='use', to='lots.Use', help_text='How is the project using the land?')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StewardProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(help_text='The name of the project using this lot.', max_length=256, verbose_name='name')),
                ('support_organization', models.CharField(help_text="What is your project's support organization, if any?", max_length=300, null=True, verbose_name='support organization', blank=True)),
                ('land_tenure_status', models.CharField(default='not sure', help_text='What is the land tenure status for the project? (This will not be shared publicly.)', max_length=50, verbose_name='land tenure status', choices=[(b'owned', 'project owns the land'), (b'licensed', 'project has a license for the land'), (b'lease', 'project has a lease for the land'), (b'access', 'project has access to the land'), (b'not sure', "I'm not sure")])),
                ('include_on_map', models.BooleanField(default=False, help_text='Can we include the project on our map?', verbose_name='include on map')),
                ('external_id', models.CharField(help_text='The external id for this project. Listed as "PROJECT ID" in some data sources.', max_length=100, null=True, verbose_name='external id', blank=True)),
                ('pilcop_garden_id', models.CharField(help_text='The pilcop garden id for this project', max_length=25, null=True, verbose_name='pilcop garden id', blank=True)),
                ('date_started', models.DateField(help_text='When did this project start?', null=True, verbose_name='date started', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('organizer', models.ForeignKey(blank=True, to='phillyorganize.Organizer', help_text='The organizer associated with this project.', null=True, verbose_name='organizer')),
                ('steward_notification', models.ForeignKey(blank=True, to='steward.StewardNotification', help_text='The notification that led to the creation of this project, if any.', null=True, verbose_name='steward notification')),
                ('use', models.ForeignKey(verbose_name='use', to='lots.Use', help_text='How is the project using the land?')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
