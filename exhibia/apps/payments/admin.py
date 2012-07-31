from django.contrib.admin import site
from payments.models import CreditPackageOrder, PaymentNotification
site.register(CreditPackageOrder)
site.register(PaymentNotification)