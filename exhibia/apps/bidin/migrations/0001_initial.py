# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuctionItem'
        db.create_table('bidin_auctionitem', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True, db_index=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('name_slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
            ('cashback1', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('cashback2', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('bidding_time', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=120)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('shipping_fee', self.gf('django.db.models.fields.FloatField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
            ('buyitnow', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('bidin', ['AuctionItem'])

        # Adding model 'AuctionItemImages'
        db.create_table('bidin_auctionitemimages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['bidin.AuctionItem'])),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bidin', ['AuctionItemImages'])


    def backwards(self, orm):
        # Deleting model 'AuctionItem'
        db.delete_table('bidin_auctionitem')

        # Deleting model 'AuctionItemImages'
        db.delete_table('bidin_auctionitemimages')


    models = {
        'bidin.auctionitem': {
            'Meta': {'object_name': 'AuctionItem'},
            'amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'bidding_time': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '120'}),
            'buyitnow': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cashback1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cashback2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shipping_fee': ('django.db.models.fields.FloatField', [], {})
        },
        'bidin.auctionitemimages': {
            'Meta': {'object_name': 'AuctionItemImages'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['bidin.AuctionItem']"})
        }
    }

    complete_apps = ['bidin']