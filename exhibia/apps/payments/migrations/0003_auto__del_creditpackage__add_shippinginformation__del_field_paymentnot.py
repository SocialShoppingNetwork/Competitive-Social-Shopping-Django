# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'CreditPackage'
        db.delete_table('payments_creditpackage')

        # Adding model 'ShippingInformation'
        db.create_table('payments_shippinginformation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(related_name='shipping', unique=True, to=orm['payments.AuctionOrder'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('tracking_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('payments', ['ShippingInformation'])

        # Deleting field 'PaymentNotification.function'
        db.delete_column('payments_paymentnotification', 'function')

        # Deleting field 'PaymentNotification.confirm'
        db.delete_column('payments_paymentnotification', 'confirm')

        # Deleting field 'PaymentNotification.received'
        db.delete_column('payments_paymentnotification', 'received')

        # Deleting field 'PaymentNotification.custom'
        db.delete_column('payments_paymentnotification', 'custom')

        # Adding field 'PaymentNotification.custom1'
        db.add_column('payments_paymentnotification', 'custom1', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Adding field 'PaymentNotification.custom2'
        db.add_column('payments_paymentnotification', 'custom2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Adding field 'PaymentNotification.created'
        db.add_column('payments_paymentnotification', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2012, 6, 20), blank=True), keep_default=False)

        # Deleting field 'CreditPackageOrder.status'
        db.delete_column('payments_creditpackageorder', 'status')

        # Deleting field 'CreditPackageOrder.price'
        db.delete_column('payments_creditpackageorder', 'price')

        # Deleting field 'CreditPackageOrder.dt'
        db.delete_column('payments_creditpackageorder', 'dt')

        # Deleting field 'CreditPackageOrder.extra_info'
        db.delete_column('payments_creditpackageorder', 'extra_info')

        # Deleting field 'CreditPackageOrder.package'
        db.delete_column('payments_creditpackageorder', 'package_id')

        # Deleting field 'CreditPackageOrder.invoice_id'
        db.delete_column('payments_creditpackageorder', 'invoice_id')

        # Deleting field 'CreditPackageOrder.transaction_id'
        db.delete_column('payments_creditpackageorder', 'transaction_id')

        # Adding field 'CreditPackageOrder.item'
        db.add_column('payments_creditpackageorder', 'item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.AuctionItem'], null=True, blank=True), keep_default=False)

        # Adding field 'CreditPackageOrder.amount_paid'
        db.add_column('payments_creditpackageorder', 'amount_paid', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'CreditPackageOrder.created'
        db.add_column('payments_creditpackageorder', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2012, 6, 20), blank=True), keep_default=False)

        # Changing field 'CreditPackageOrder.pn'
        db.alter_column('payments_creditpackageorder', 'pn_id', self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.date(2012, 6, 20), to=orm['payments.PaymentNotification']))

        # Deleting field 'AuctionOrder.shipping_fee'
        db.delete_column('payments_auctionorder', 'shipping_fee')

        # Deleting field 'AuctionOrder.invoice_id'
        db.delete_column('payments_auctionorder', 'invoice_id')

        # Deleting field 'AuctionOrder.carrier'
        db.delete_column('payments_auctionorder', 'carrier')

        # Deleting field 'AuctionOrder.tracking_number'
        db.delete_column('payments_auctionorder', 'tracking_number')

        # Deleting field 'AuctionOrder.address'
        db.delete_column('payments_auctionorder', 'address')

        # Deleting field 'AuctionOrder.total'
        db.delete_column('payments_auctionorder', 'total')

        # Deleting field 'AuctionOrder.transaction_id'
        db.delete_column('payments_auctionorder', 'transaction_id')

        # Deleting field 'AuctionOrder.discount_amount'
        db.delete_column('payments_auctionorder', 'discount_amount')

        # Adding field 'AuctionOrder.amount_paid'
        db.add_column('payments_auctionorder', 'amount_paid', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Changing field 'AuctionOrder.status'
        db.alter_column('payments_auctionorder', 'status', self.gf('django.db.models.fields.CharField')(max_length=3))

        # Changing field 'AuctionOrder.method'
        db.alter_column('payments_auctionorder', 'method', self.gf('django.db.models.fields.CharField')(max_length=3))


    def backwards(self, orm):
        
        # Adding model 'CreditPackage'
        db.create_table('payments_creditpackage', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True, db_index=True)),
            ('credits', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('contract_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bonus', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('payments', ['CreditPackage'])

        # Deleting model 'ShippingInformation'
        db.delete_table('payments_shippinginformation')

        # Adding field 'PaymentNotification.function'
        db.add_column('payments_paymentnotification', 'function', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'PaymentNotification.confirm'
        db.add_column('payments_paymentnotification', 'confirm', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'PaymentNotification.received'
        raise RuntimeError("Cannot reverse this migration. 'PaymentNotification.received' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'PaymentNotification.custom'
        raise RuntimeError("Cannot reverse this migration. 'PaymentNotification.custom' and its values cannot be restored.")

        # Deleting field 'PaymentNotification.custom1'
        db.delete_column('payments_paymentnotification', 'custom1')

        # Deleting field 'PaymentNotification.custom2'
        db.delete_column('payments_paymentnotification', 'custom2')

        # Deleting field 'PaymentNotification.created'
        db.delete_column('payments_paymentnotification', 'created')

        # User chose to not deal with backwards NULL issues for 'CreditPackageOrder.status'
        raise RuntimeError("Cannot reverse this migration. 'CreditPackageOrder.status' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CreditPackageOrder.price'
        raise RuntimeError("Cannot reverse this migration. 'CreditPackageOrder.price' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CreditPackageOrder.dt'
        raise RuntimeError("Cannot reverse this migration. 'CreditPackageOrder.dt' and its values cannot be restored.")

        # Adding field 'CreditPackageOrder.extra_info'
        db.add_column('payments_creditpackageorder', 'extra_info', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'CreditPackageOrder.package'
        raise RuntimeError("Cannot reverse this migration. 'CreditPackageOrder.package' and its values cannot be restored.")

        # Adding field 'CreditPackageOrder.invoice_id'
        db.add_column('payments_creditpackageorder', 'invoice_id', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Adding field 'CreditPackageOrder.transaction_id'
        db.add_column('payments_creditpackageorder', 'transaction_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Deleting field 'CreditPackageOrder.item'
        db.delete_column('payments_creditpackageorder', 'item_id')

        # Deleting field 'CreditPackageOrder.amount_paid'
        db.delete_column('payments_creditpackageorder', 'amount_paid')

        # Deleting field 'CreditPackageOrder.created'
        db.delete_column('payments_creditpackageorder', 'created')

        # Changing field 'CreditPackageOrder.pn'
        db.alter_column('payments_creditpackageorder', 'pn_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.PaymentNotification'], null=True))

        # Adding field 'AuctionOrder.shipping_fee'
        db.add_column('payments_auctionorder', 'shipping_fee', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'AuctionOrder.invoice_id'
        db.add_column('payments_auctionorder', 'invoice_id', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Adding field 'AuctionOrder.carrier'
        db.add_column('payments_auctionorder', 'carrier', self.gf('django.db.models.fields.CharField')(default='UPS', max_length=20, blank=True), keep_default=False)

        # Adding field 'AuctionOrder.tracking_number'
        db.add_column('payments_auctionorder', 'tracking_number', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'AuctionOrder.address'
        raise RuntimeError("Cannot reverse this migration. 'AuctionOrder.address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AuctionOrder.total'
        raise RuntimeError("Cannot reverse this migration. 'AuctionOrder.total' and its values cannot be restored.")

        # Adding field 'AuctionOrder.transaction_id'
        db.add_column('payments_auctionorder', 'transaction_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'AuctionOrder.discount_amount'
        db.add_column('payments_auctionorder', 'discount_amount', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Deleting field 'AuctionOrder.amount_paid'
        db.delete_column('payments_auctionorder', 'amount_paid')

        # Changing field 'AuctionOrder.status'
        db.alter_column('payments_auctionorder', 'status', self.gf('django.db.models.fields.CharField')(max_length=1))

        # Changing field 'AuctionOrder.method'
        db.alter_column('payments_auctionorder', 'method', self.gf('django.db.models.fields.CharField')(max_length=1))


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
            'amount_paid': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.Auction']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '3'}),
            'pn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.PaymentNotification']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '3'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Member']"})
        },
        'payments.creditpackageorder': {
            'Meta': {'ordering': "['-id']", 'object_name': 'CreditPackageOrder'},
            'amount_paid': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['profiles.Member']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auctions.AuctionItem']", 'null': 'True', 'blank': 'True'}),
            'pn': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.PaymentNotification']"})
        },
        'payments.paymentnotification': {
            'Meta': {'ordering': "['-created']", 'object_name': 'PaymentNotification'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'custom1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'custom2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'item_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mc_gross': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'payer_email': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'request_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shipping': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'payments.shippinginformation': {
            'Meta': {'object_name': 'ShippingInformation'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'shipping'", 'unique': 'True', 'to': "orm['payments.AuctionOrder']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
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
