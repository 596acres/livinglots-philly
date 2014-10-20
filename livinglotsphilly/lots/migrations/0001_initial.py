# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('availableproperties', '0001_initial'),
        ('taxaccounts', '0001_initial'),
        ('landuse', '0001_initial'),
        ('parcels', '0001_initial'),
        ('owners', '0001_initial'),
        ('violations', '0003_auto_20141015_1947'),
        ('waterdept', '0001_initial'),
        ('opa', '0001_initial'),
        ('zoning', '0001_initial'),
        ('boundaries', '__first__'),
        ('licenses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('centroid', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, verbose_name='centroid', blank=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, verbose_name='polygon', blank=True)),
                ('name', models.CharField(max_length=256, null=True, verbose_name='name', blank=True)),
                ('address_line1', models.CharField(max_length=150, null=True, verbose_name='address line 1', blank=True)),
                ('address_line2', models.CharField(max_length=150, null=True, verbose_name='address line 2', blank=True)),
                ('postal_code', models.CharField(max_length=10, null=True, verbose_name='postal code', blank=True)),
                ('city', models.CharField(max_length=50, null=True, verbose_name='city', blank=True)),
                ('state_province', models.CharField(max_length=40, null=True, verbose_name='state/province', blank=True)),
                ('country', models.CharField(max_length=40, null=True, verbose_name='country', blank=True)),
                ('known_use_certainty', models.PositiveIntegerField(default=0, help_text='On a scale of 0 to 10, how certain are we that the known use is correct?', verbose_name='known use certainty')),
                ('known_use_locked', models.BooleanField(default=False, help_text='Is the known use field locked? If it is not, the site will make a guess using available data. If you are certain that the known use is correct, lock it.', verbose_name='known use locked')),
                ('added', models.DateTimeField(help_text=b'When this lot was added', verbose_name='date added', auto_now_add=True)),
                ('steward_inclusion_opt_in', models.BooleanField(default=False, help_text='Did the steward opt in to being included on our map?', verbose_name='steward inclusion opt-in')),
                ('polygon_area', models.DecimalField(decimal_places=2, max_digits=15, blank=True, help_text='The area of the polygon in square feet', null=True, verbose_name='polygon area')),
                ('polygon_width', models.DecimalField(decimal_places=2, max_digits=10, blank=True, help_text='The width of the polygon in feet', null=True, verbose_name='polygon width')),
                ('polygon_tied_to_parcel', models.BooleanField(default=True, help_text="Is the polygon of this lot always matched up with the parcel's polygon on save?", verbose_name='polygon tied to parcel')),
            ],
            options={
                'permissions': (('view_all_details', 'Can view all details for lots'), ('view_all_filters', 'Can view all map filters for lots'), ('view_all_lots', 'Can view all lots')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LotGroup',
            fields=[
                ('lot_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='lots.Lot')),
            ],
            options={
                'abstract': False,
            },
            bases=('lots.lot',),
        ),
        migrations.CreateModel(
            name='Use',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(max_length=200, verbose_name='slug')),
                ('visible', models.BooleanField(default=True, help_text='Should lots with this use be visible on the map? If the use is not vacant and not a project that someone could join, probably not.', verbose_name='visible')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lot',
            name='available_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='availableproperties.AvailableProperty', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='billing_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='opa.BillingAccount', help_text="The owner's billing account for this lot.", null=True, verbose_name='billing account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='city_council_district',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='city council district', blank=True, to='boundaries.Boundary', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='group', blank=True, to='lots.LotGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='known_use',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='lots.Use', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='land_use_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='landuse.LandUseArea', help_text='The land use area for this lot.', null=True, verbose_name='land use'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='licenses',
            field=models.ManyToManyField(help_text='The licenses associated with this lot.', to='licenses.License', null=True, verbose_name='licenses', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='owners.Owner', help_text='The owner of this lot.', null=True, verbose_name='owner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='parcel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='parcels.Parcel', help_text='The parcel this lot is based on.', null=True, verbose_name='parcel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='planning_district',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='planning district', blank=True, to='boundaries.Boundary', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='tax_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='taxaccounts.TaxAccount', help_text='The tax account for this lot.', null=True, verbose_name='tax account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='violations',
            field=models.ManyToManyField(help_text='The violations associated with this lot.', to='violations.Violation', null=True, verbose_name='violations', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='water_parcel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='waterdept.WaterParcel', help_text='The parcel the Water Department defines for this lot', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='zoning_district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='zoning district', blank=True, to='zoning.BaseDistrict', null=True),
            preserve_default=True,
        ),
    ]
