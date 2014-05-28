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
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['auth.User'])),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.Auction'])),
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

        # Adding unique constraint on 'Order', fields ['user', 'auction']
        db.create_unique('checkout_order', ['user_id', 'auction_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Order', fields ['user', 'auction']
        db.delete_unique('checkout_order', ['user_id', 'auction_id'])

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
        'auctions.auctionbid': {
            'Meta': {'object_name': 'AuctionBid'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bids'", 'to': "orm['auctions.Auction']"}),
            'bidder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'unixtime': ('django.db.models.fields.FloatField', [], {})
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
        'auctions.auctionplegde': {
            'Meta': {'object_name': 'AuctionPlegde'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.Auction']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']"})
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
            'points_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'referral_url': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invited_users'", 'null': 'True', 'to': "orm['referrals.ReferralLink']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'referrals.referrallink': {
            'Meta': {'object_name': 'ReferralLink'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'redirect_to': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '500'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'refferal_urls'", 'to': "orm['auth.User']"}),
            'visit_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['auctions']
