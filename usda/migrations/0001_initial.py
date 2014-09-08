# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Food'
        db.create_table(u'usda_food', (
            ('ndb_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('food_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.FoodGroup'])),
            ('long_description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('manufacturer_name', self.gf('django.db.models.fields.CharField')(max_length=65, blank=True)),
            ('survey', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('refuse_description', self.gf('django.db.models.fields.CharField')(max_length=135, blank=True)),
            ('refuse_percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('scientific_name', self.gf('django.db.models.fields.CharField')(max_length=65, blank=True)),
            ('nitrogen_factor', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('protein_factor', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('fat_factor', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cho_factor', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'usda', ['Food'])

        # Adding model 'FoodGroup'
        db.create_table(u'usda_foodgroup', (
            ('code', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
        ))
        db.send_create_signal(u'usda', ['FoodGroup'])

        # Adding model 'Nutrient'
        db.create_table(u'usda_nutrient', (
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('tagname', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('decimals', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'usda', ['Nutrient'])

        # Adding model 'NutrientData'
        db.create_table(u'usda_nutrientdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.Food'])),
            ('nutrient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.Nutrient'])),
            ('nutrient_value', self.gf('django.db.models.fields.FloatField')()),
            ('data_points', self.gf('django.db.models.fields.IntegerField')()),
            ('standard_error', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('data_derivation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.DataDerivation'], null=True, blank=True)),
            ('reference_nbd_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('added_nutrient', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number_of_studies', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('minimum', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('maximum', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('degrees_of_freedom', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lower_error_bound', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('upper_error_bound', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('statistical_comments', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('confidence_code', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal(u'usda', ['NutrientData'])

        # Adding unique constraint on 'NutrientData', fields ['food', 'nutrient']
        db.create_unique(u'usda_nutrientdata', ['food_id', 'nutrient_id'])

        # Adding M2M table for field source on 'NutrientData'
        db.create_table(u'usda_nutrientdata_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nutrientdata', models.ForeignKey(orm[u'usda.nutrientdata'], null=False)),
            ('source', models.ForeignKey(orm[u'usda.source'], null=False))
        ))
        db.create_unique(u'usda_nutrientdata_source', ['nutrientdata_id', 'source_id'])

        # Adding model 'Source'
        db.create_table(u'usda_source', (
            ('code', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'usda', ['Source'])

        # Adding model 'DataDerivation'
        db.create_table(u'usda_dataderivation', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'usda', ['DataDerivation'])

        # Adding model 'Weight'
        db.create_table(u'usda_weight', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.Food'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('gram_weight', self.gf('django.db.models.fields.FloatField')()),
            ('number_of_data_points', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('standard_deviation', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'usda', ['Weight'])

        # Adding unique constraint on 'Weight', fields ['food', 'sequence']
        db.create_unique(u'usda_weight', ['food_id', 'sequence'])

        # Adding model 'Footnote'
        db.create_table(u'usda_footnote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.Food'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('nutrient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usda.Nutrient'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'usda', ['Footnote'])

        # Adding unique constraint on 'Footnote', fields ['food', 'number', 'nutrient']
        db.create_unique(u'usda_footnote', ['food_id', 'number', 'nutrient_id'])

        # Adding model 'DataSource'
        db.create_table(u'usda_datasource', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=6, primary_key=True)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=135, null=True, blank=True)),
            ('volume_or_city', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('issue_or_state', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('start_page', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('end_page', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'usda', ['DataSource'])


    def backwards(self, orm):
        # Removing unique constraint on 'Footnote', fields ['food', 'number', 'nutrient']
        db.delete_unique(u'usda_footnote', ['food_id', 'number', 'nutrient_id'])

        # Removing unique constraint on 'Weight', fields ['food', 'sequence']
        db.delete_unique(u'usda_weight', ['food_id', 'sequence'])

        # Removing unique constraint on 'NutrientData', fields ['food', 'nutrient']
        db.delete_unique(u'usda_nutrientdata', ['food_id', 'nutrient_id'])

        # Deleting model 'Food'
        db.delete_table(u'usda_food')

        # Deleting model 'FoodGroup'
        db.delete_table(u'usda_foodgroup')

        # Deleting model 'Nutrient'
        db.delete_table(u'usda_nutrient')

        # Deleting model 'NutrientData'
        db.delete_table(u'usda_nutrientdata')

        # Removing M2M table for field source on 'NutrientData'
        db.delete_table('usda_nutrientdata_source')

        # Deleting model 'Source'
        db.delete_table(u'usda_source')

        # Deleting model 'DataDerivation'
        db.delete_table(u'usda_dataderivation')

        # Deleting model 'Weight'
        db.delete_table(u'usda_weight')

        # Deleting model 'Footnote'
        db.delete_table(u'usda_footnote')

        # Deleting model 'DataSource'
        db.delete_table(u'usda_datasource')


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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usda.Food']"}),
            'gram_weight': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_data_points': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'standard_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['usda']