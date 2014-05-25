# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table('checkout_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('auction', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auctions.Auction'], unique=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.Card'])),
            ('tracking_number', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('shipping_company', self.gf('django.db.models.fields.CharField')(default=True, max_length=5, blank=True)),
            ('shipping_fee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.ShippingFee'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='op', max_length=2)),
            ('shipping_first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shipping_last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shipping_address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shipping_address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('shipping_city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shipping_state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('shipping_country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('shipping_zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('shipping_phone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('billing_first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('billing_last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('billing_address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('billing_address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('billing_city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('billing_state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('billing_country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('billing_zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('billing_phone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('checkout', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table('checkout_order')


    models = {
        'auctions.auction': {
            'Meta': {'object_name': 'Auction'},
            'amount_pleged': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'backers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bidding_time': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_offer': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'deadline_time': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'ended_unixtime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_queue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auctions'", 'to': "orm['auctions.AuctionItem']"}),
            'last_bid_type': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'last_bidder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'db_index': 'True', 'blank': 'True'}),
            'last_bidder_member': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_won'", 'null': 'True', 'to': "orm['auth.User']"}),
            'last_unixtime': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pledge_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '43200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '2', 'db_index': 'True'})
        },
        'auctions.auctionitem': {
            'Meta': {'object_name': 'AuctionItem'},
            'amount': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bidding_time': ('django.db.models.fields.SmallIntegerField', [], {'default': '120'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.Brand']", 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auctions.Category']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'default': "''", 'blank': 'True'}),
            'giveaway': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auctions.AuctionItemImages']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'lock_after': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'newbie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'pledge_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '180'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'shipping_fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250'})
        },
        'auctions.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250'})
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
        'checkout.order': {
            'Meta': {'object_name': 'Order'},
            'auction': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auctions.Auction']", 'unique': 'True'}),
            'billing_address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'billing_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'billing_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'billing_phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'billing_state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'billing_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.Card']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shipping_address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'shipping_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_company': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '5', 'blank': 'True'}),
            'shipping_country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'shipping_fee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.ShippingFee']"}),
            'shipping_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shipping_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shipping_phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'shipping_state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'shipping_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'op'", 'max_length': '2'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'payments.card': {
            'Meta': {'object_name': 'Card'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expiration_month': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'expiration_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'holder_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'shipping.shippingfee': {
            'Meta': {'object_name': 'ShippingFee'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shipping_fees'", 'to': "orm['auctions.AuctionItem']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'shipping': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['checkout']