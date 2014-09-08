# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Weight.description'
        db.alter_column(u'usda_weight', 'description', self.gf('django.db.models.fields.CharField')(max_length=84))

    def backwards(self, orm):

        # Changing field 'Weight.description'
        db.alter_column(u'usda_weight', 'description', self.gf('django.db.models.fields.CharField')(max_length=80))

    models = {
        u'usda.dataderivation': {
            'Meta': {'ordering': "['code']", 'object_name': 'DataDerivation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'usda.datasource': {
            'Meta': {'ordering': "['id']", 'object_name': 'DataSource'},
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'issue_or_state': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '135', 'null': 'True', 'blank': 'True'}),
            'start_page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume_or_city': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'usda.food': {
            'Meta': {'ordering': "['ndb_number']", 'object_name': 'Food'},
            'cho_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'fat_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'food_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.FoodGroup']"}),
            'long_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'manufacturer_name': ('django.db.models.fields.CharField', [], {'max_length': '65', 'blank': 'True'}),
            'ndb_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nitrogen_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'protein_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'refuse_description': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'}),
            'refuse_percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '65', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'survey': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'usda.foodgroup': {
            'Meta': {'ordering': "['code']", 'object_name': 'FoodGroup'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        },
        u'usda.footnote': {
            'Meta': {'ordering': "['food', 'number']", 'unique_together': "(['food', 'number', 'nutrient'],)", 'object_name': 'Footnote'},
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.Food']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'nutrient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.Nutrient']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'usda.nutrient': {
            'Meta': {'ordering': "['number']", 'object_name': 'Nutrient'},
            'decimals': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'tagname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        u'usda.nutrientdata': {
            'Meta': {'ordering': "['food', 'nutrient']", 'unique_together': "(['food', 'nutrient'],)", 'object_name': 'NutrientData'},
            'added_nutrient': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confidence_code': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'data_derivation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.DataDerivation']", 'null': 'True', 'blank': 'True'}),
            'data_points': ('django.db.models.fields.IntegerField', [], {}),
            'degrees_of_freedom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.Food']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lower_error_bound': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'maximum': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'minimum': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_studies': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nutrient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.Nutrient']"}),
            'nutrient_value': ('django.db.models.fields.FloatField', [], {}),
            'reference_nbd_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['usda.Source']", 'symmetrical': 'False'}),
            'standard_error': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'statistical_comments': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'upper_error_bound': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'usda.source': {
            'Meta': {'ordering': "['code']", 'object_name': 'Source'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'usda.weight': {
            'Meta': {'ordering': "['food', 'sequence']", 'unique_together': "(['food', 'sequence'],)", 'object_name': 'Weight'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '84'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.Food']"}),
            'gram_weight': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_data_points': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'standard_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['usda']