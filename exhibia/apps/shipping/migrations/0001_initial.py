# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShippingAddress'
        db.create_table('shipping_shippingaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Member'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('shipping', ['ShippingAddress'])

        # Adding model 'ShippingFee'
        db.create_table('shipping_shippingfee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.AuctionItem'])),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('shipping', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('shipping', ['ShippingFee'])

        # Adding model 'ShippingRequest'
        db.create_table('shipping_shippingrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Member'])),
            ('auction', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auctions.Auction'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('waiting', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('shipping', ['ShippingRequest'])

        # Adding unique constraint on 'ShippingRequest', fields ['member', 'auction']
        db.create_unique('shipping_shippingrequest', ['member_id', 'auction_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ShippingRequest', fields ['member', 'auction']
        db.delete_unique('shipping_shippingrequest', ['member_id', 'auction_id'])

        # Deleting model 'ShippingAddress'
        db.delete_table('shipping_shippingaddress')

        # Deleting model 'ShippingFee'
        db.delete_table('shipping_shippingfee')

        # Deleting model 'ShippingRequest'
        db.delete_table('shipping_shippingrequest')


    models = {
        'auctions.auction': {
            'Meta': {'object_name': 'Auction'},
            'amount_pleged': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'backers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bidding_time': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_offer': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'deadline_time': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'ended_unixtime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auctions'", 'to': "orm['auctions.AuctionItem']"}),
            'last_bid_type': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'last_bidder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'db_index': 'True'}),
            'last_bidder_member': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_won'", 'null': 'True', 'to': "orm['profiles.Member']"}),
            'last_unixtime': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'pledge_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '43200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '2', 'db_index': 'True'})
        },
        'auctions.auctionitem': {
            'Meta': {'object_name': 'AuctionItem'},
            'amount': ('django.db.models.fields.SmallIntegerField', [], {}),
            'bidding_time': ('django.db.models.fields.SmallIntegerField', [], {'default': '120'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.Brand']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.Category']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': "''"}),
            'image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auctions.AuctionItemImages']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'pledge_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '180'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shipping_fee': ('django.db.models.fields.FloatField', [], {}),
            'showcase_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600'}),
            'slug_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'auctions.auctionitemimages': {
            'Meta': {'object_name': 'AuctionItemImages'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['auctions.AuctionItem']"})
        },
        'auctions.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'auctions.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.member': {
            'Meta': {'object_name': 'Member'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'credits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'shipping.shippingaddress': {
            'Meta': {'object_name': 'ShippingAddress'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'shipping.shippingfee': {
            'Meta': {'object_name': 'ShippingFee'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.AuctionItem']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shipping': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'shipping.shippingrequest': {
            'Meta': {'unique_together': "(('member', 'auction'),)", 'object_name': 'ShippingRequest'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'auction': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auctions.Auction']", 'unique': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'waiting': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['shipping']