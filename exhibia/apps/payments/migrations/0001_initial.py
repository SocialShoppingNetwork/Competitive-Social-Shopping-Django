# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PaymentNotification'
        db.create_table('payments_paymentnotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('item_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('item_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('quantity', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('shipping', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('payer_email', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('mc_gross', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('custom', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('request_log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('confirm', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('payments', ['PaymentNotification'])

        # Adding model 'CreditPackage'
        db.create_table('payments_creditpackage', (
            ('contract_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('credits', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('bonus', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('payments', ['CreditPackage'])

        # Adding model 'CreditPackageOrder'
        db.create_table('payments_creditpackageorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['payments.CreditPackage'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['profiles.Member'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('invoice_id', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('pn', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.PaymentNotification'], null=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('payments', ['CreditPackageOrder'])

        # Adding model 'AuctionOrder'
        db.create_table('payments_auctionorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.Auction'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Member'])),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('item_price', self.gf('django.db.models.fields.FloatField')()),
            ('shipping_fee', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('total', self.gf('django.db.models.fields.FloatField')()),
            ('discount_amount', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('method', self.gf('django.db.models.fields.CharField')(default='p', max_length=1)),
            ('invoice_id', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='n', max_length=1)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('pn', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.PaymentNotification'], null=True, blank=True)),
            ('carrier', self.gf('django.db.models.fields.CharField')(default='UPS', max_length=20, blank=True)),
            ('tracking_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('payments', ['AuctionOrder'])


    def backwards(self, orm):
        
        # Deleting model 'PaymentNotification'
        db.delete_table('payments_paymentnotification')

        # Deleting model 'CreditPackage'
        db.delete_table('payments_creditpackage')

        # Deleting model 'CreditPackageOrder'
        db.delete_table('payments_creditpackageorder')

        # Deleting model 'AuctionOrder'
        db.delete_table('payments_auctionorder')


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
            'last_bidder_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']", 'null': 'True', 'blank': 'True'}),
            'last_unixtime': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'pledge_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '43200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '1', 'db_index': 'True'})
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
        'payments.auctionorder': {
            'Meta': {'ordering': "['-id']", 'object_name': 'AuctionOrder'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.Auction']"}),
            'carrier': ('django.db.models.fields.CharField', [], {'default': "'UPS'", 'max_length': '20', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'discount_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'item_price': ('django.db.models.fields.FloatField', [], {}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1'}),
            'pn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.PaymentNotification']", 'null': 'True', 'blank': 'True'}),
            'shipping_fee': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'total': ('django.db.models.fields.FloatField', [], {}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']"})
        },
        'payments.creditpackage': {
            'Meta': {'ordering': "['price']", 'object_name': 'CreditPackage'},
            'bonus': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True', 'db_index': 'True'}),
            'contract_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'credits': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        'payments.creditpackageorder': {
            'Meta': {'ordering': "['-id']", 'object_name': 'CreditPackageOrder'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['profiles.Member']"}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['payments.CreditPackage']"}),
            'pn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.PaymentNotification']", 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'payments.paymentnotification': {
            'Meta': {'ordering': "['-received']", 'object_name': 'PaymentNotification'},
            'confirm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'custom': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'item_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mc_gross': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'payer_email': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'request_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shipping': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25'})
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
            'location': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['payments']
