from payments.gateways import PaymentGateway
from payments.models import PaymentNotification, CreditPackage

from django.conf import settings
from django.utils import simplejson
from django.contrib.sites.models import Site

# payment notification status
CREDITS = 'credits'
AUCTION = 'auction'
BUYITNOW = 'buyitnow'

CONFIRMED = "Confirmed"
SUSPENDED = "Suspended"
FAILED = "Failed"

class PlimusGateway(PaymentGateway):
    def __init__(self, *args, **kwargs):
        super(PlimusGateway, self).__init__(*args, **kwargs)

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

        st = data['transactionType']
        pn = PaymentNotification(
            token = data['referenceNumber'], # referenceNumber Number Plimus Reference Number
            type = 'Plimus',
            status = st,
            payer_email = data['email'], # email String Customer email address
            quantity = data['quantity'], # quantity Number Quantity ordered
            mc_gross = data['contractPrice'],  # contractPrice Number #,###.## Contract price
            item_name = data['item_name'],
            item_number = data['item_number'],
            custom = data['member'],
            request_log = str(self.request),
            data = simplejson.dumps(data),
        )
        pn.confirm = (st == "CHARGE" or st == "RECURRING") and CONFIRMED or '%s: %s' % (FAILED, pn.status)
        # contractId Number Plimus Contract Id
        if int(data['contractId']) in CreditPackage.objects.values_list('contract_id', flat=True):
            pn.function = CREDITS
        else:
            pn.function = AUCTION
        pn.save()
        return pn
    
    def get_url(self):
        return self.merchant['call_url']
