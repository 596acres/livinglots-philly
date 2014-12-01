# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waterdept', '0001_initial'),
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendlyOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email', blank=True)),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='phone', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='notes', blank=True)),
                ('added', models.DateTimeField(help_text=b'When this record was added', verbose_name='date added', auto_now_add=True)),
                ('lot', models.ForeignKey(blank=True, to='lots.Lot', null=True)),
                ('parcels', models.ManyToManyField(to='waterdept.WaterParcel')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
