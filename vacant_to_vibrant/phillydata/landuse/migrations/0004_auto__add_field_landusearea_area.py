# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LandUseArea.area'
        db.add_column(u'landuse_landusearea', 'area',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'LandUseArea.area'
        db.delete_column(u'landuse_landusearea', 'area')


    models = {
        u'landuse.landusearea': {
            'Meta': {'object_name': 'LandUseArea'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'vacant_building': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['landuse']