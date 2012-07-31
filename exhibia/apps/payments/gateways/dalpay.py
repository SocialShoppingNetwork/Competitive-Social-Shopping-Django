from payments.gateways import PaymentGateway
from payments.models import PaymentNotification
from auctions.constants import *
from payments.constants import *
from django.conf import settings
from django.utils import simplejson
from django.contrib.sites.models import Site

class DalpayGateway(PaymentGateway):

    def __init__(self, *args, **kwargs):
        super(DalpayGateway, self).__init__(*args, **kwargs)
        self.contract_id = settings.DALPAY_MERCHANT_ID

    def verify(self):
        return True

    def create_payment_notification(self):
        # transactionType String:
        #   AUTH_ONLY - orders that were authorized for a future charge
        #   CHARGE - orders that were successfully charged
        #   REFUND - orders that were refunded
        #   CHARGEBACK - ordered that were charged back by the customer
        #   CANCELLATION - orders that were cancelled (for unapproved orders and cancelled subscriptions)
        #   RECURRING - subscription orders that were successfully charged
        #   CANCELLATION_REFUND - orders that were refunded and cancelled (for cancelled subscriptions)
        #   CONTRACT_CHANGE - subscription orders that had their contract switched

        data = self.data

        pn = PaymentNotification(
            site = Site.objects.get_current(),
            token = data['SilentPostPassword'], # referenceNumber Number Plimus Reference Number
            type = 'DalPay',
            status = CONFIRMED,
            payer_email = data['cust_email'], # email String Customer email address
            quantity = '1', # quantity Number Quantity ordered
            mc_gross = data['total_amount'],  # contractPrice Number #,###.## Contract price
            item_name = data['item1_desc'],
            item_number = data['user2'],
            custom = data['user1']    ,
            request_log = str(self.request),
            data=simplejson.dumps(data),
        )
        #pn.confirm = (st == "CHARGE" or st == "RECURRING") and CONFIRMED or '%s: %s' % (FAILED, pn.status)
        pn.confirm = CONFIRMED
        if 'credits' in kwargs:
            pn.function = CREDITS
        else:
            pn.function = AUCTION
        pn.save()
        return pn

    def get_url(self):
        return self.merchant['call_url']