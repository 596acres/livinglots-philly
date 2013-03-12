# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TaxAccount.market_value'
        db.alter_column(u'taxaccounts_taxaccount', 'market_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2))

        # Changing field 'TaxAccount.exempt_abate_assessment'
        db.alter_column(u'taxaccounts_taxaccount', 'exempt_abate_assessment', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2))

        # Changing field 'TaxAccount.amount_delinquent'
        db.alter_column(u'taxaccounts_taxaccount', 'amount_delinquent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'TaxAccount.market_value'
        db.alter_column(u'taxaccounts_taxaccount', 'market_value', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2))

        # Changing field 'TaxAccount.exempt_abate_assessment'
        db.alter_column(u'taxaccounts_taxaccount', 'exempt_abate_assessment', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2))

        # Changing field 'TaxAccount.amount_delinquent'
        db.alter_column(u'taxaccounts_taxaccount', 'amount_delinquent', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2))

    models = {
        u'opa.accountowner': {
            'Meta': {'object_name': 'AccountOwner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['owners.Owner']", 'null': 'True', 'blank': 'True'})
        },
        u'opa.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'account_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opa.AccountOwner']", 'null': 'True', 'blank': 'True'}),
            'assessment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'improvement_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'land_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '3', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mailing_country': ('django.db.models.fields.CharField', [], {'default': "'USA'", 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mailing_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mailing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mailing_state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'property_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'sale_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'owners.agencycode': {
            'Meta': {'object_name': 'AgencyCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'owners.alias': {
            'Meta': {'object_name': 'Alias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'agency_codes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['owners.AgencyCode']", 'null': 'True', 'blank': 'True'}),
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['owners.Alias']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'})
        },
        u'taxaccounts.taxaccount': {
            'Meta': {'object_name': 'TaxAccount'},
            'amount_delinquent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opa.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'brt_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'building_category': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'building_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'exempt_abate_assessment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'market_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'max_period': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'min_period': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'owner_name2': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'property_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'property_city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'property_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'property_state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'taxable_assessment': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'years_delinquent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['taxaccounts']