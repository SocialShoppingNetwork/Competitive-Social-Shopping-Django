from django.test import TestCase
#from django.utils import unittest
from payments.views import order_plimus
from django.test.client import Client
from payments.models import CreditPackage, CreditPackageOrder
from profiles.models import Member
from payments.constants import *
class AnimalTestCase(TestCase):
    fixtures = ['users.json', 'packages.json',]
    def setUp(self):
        self.client = Client()

    def test_paid_ok(self):
        data = {'accountId': ['19328970'],
        'addCD': ['N'],
        'address1': ['6626 W 93rd St'],
        'authKey': ['bb2d2b0c272cfce1890cb06da0e4331b'],
        'city': ['Oak Lawn'],
        'contractId': ['10'],
        'contractName': ['10 Bids Package'],
        'contractOwner': ['380018'],
        'contractPrice': ['10.00'],
        'country': ['US'],
        'creditCardExpDate': ['12/2011'],
        'creditCardLastFourDigits': ['1111'],
        'creditCardType': ['VISA'],
        'currency': ['USD'],
        'email': ['xtealc@gmail.com'],
        'firstName': ['John'],
        'invoiceAddress1': ['6626 W 93rd St'],
        'invoiceAmount': ['10.00'],
        'invoiceAmountUSD': ['10.00'],
        'invoiceChargeAmount': ['10.00'],
        'invoiceChargeCurrency': ['USD'],
        'invoiceCity': ['Oak Lawn'],
        'invoiceCountry': ['US'],
        'invoiceEmail': ['xtealc@gmail.com'],
        'invoiceFirstName': ['John'],
        'invoiceInfoURL': ['https://sandbox.plimus.com/jsp/order_locator_info.jsp?refId=E25D2B5B70E661B02BB5D14C1704EE0C&acd=F12B83314E814509'],
        'invoiceLastName': ['Doe'],
        'invoiceState': ['ID'],
        'invoiceWorkPhone': ['18583507473'],
        'invoiceZipCode': ['60453'],
        'lastName': ['Doe'],
        'licenseKey': ['\n'],
        'paymentMethod': ['CC'],
        'paymentType': ['CC'],
        'productId': ['289490'],
        'productName': ['Exhibia'],
        'promoteContractsNum': ['0'],
        'quantity': ['1'],
        'referenceNumber': ['1002906620'],
        'remoteAddress': ['186.113.118.234'],
        'shippingAddress1': ['6626 W 93rd St'],
        'shippingCity': ['Oak Lawn'],
        'shippingCountry': ['US'],
        'shippingFirstName': ['John'],
        'shippingLastName': ['Doe'],
        'shippingState': ['ID'],
        'shippingZipCode': ['60453'],
        'state': ['ID'],
        'targetBalance': ['PLIMUS_ACCOUNT'],
        'testMode': ['N'],
        'transactionDate': ['12/08/2011 02:38 PM'],
        'transactionType': ['CHARGE'],
        'untilDate': ['12/08/2011 02:38 PM'],
        'username': ['1323383684612'],
        'workPhone': ['18583507473'],
        'zipCode': ['60453'],
        'item_number': 'PCKG10',
        'item_name': 'Credit Package 10',
        'member':'vh5'}
        member = Member.objects.get(user__username=data['member'])
        package = CreditPackage.objects.get(code=data['item_number'])
        credits = member.credits
        self.client.post('/pay/package/plimus/', data)
        member = Member.objects.get(user__username=data['member'])
        self.assertEqual(member.credits, credits + package.total_credits)

    def test_paid_less(self):
        data = {'accountId': ['19328970'],
        'addCD': ['N'],
        'address1': ['6626 W 93rd St'],
        'authKey': ['bb2d2b0c272cfce1890cb06da0e4331b'],
        'city': ['Oak Lawn'],
        'contractId': ['10'],
        'contractName': ['10 Bids Package'],
        'contractOwner': ['380018'],
        'contractPrice': ['5.00'],
        'country': ['US'],
        'creditCardExpDate': ['12/2011'],
        'creditCardLastFourDigits': ['1111'],
        'creditCardType': ['VISA'],
        'currency': ['USD'],
        'email': ['xtealc@gmail.com'],
        'firstName': ['John'],
        'invoiceAddress1': ['6626 W 93rd St'],
        'invoiceAmount': ['10.00'],
        'invoiceAmountUSD': ['10.00'],
        'invoiceChargeAmount': ['10.00'],
        'invoiceChargeCurrency': ['USD'],
        'invoiceCity': ['Oak Lawn'],
        'invoiceCountry': ['US'],
        'invoiceEmail': ['xtealc@gmail.com'],
        'invoiceFirstName': ['John'],
        'invoiceInfoURL': ['https://sandbox.plimus.com/jsp/order_locator_info.jsp?refId=E25D2B5B70E661B02BB5D14C1704EE0C&acd=F12B83314E814509'],
        'invoiceLastName': ['Doe'],
        'invoiceState': ['ID'],
        'invoiceWorkPhone': ['18583507473'],
        'invoiceZipCode': ['60453'],
        'lastName': ['Doe'],
        'licenseKey': ['\n'],
        'paymentMethod': ['CC'],
        'paymentType': ['CC'],
        'productId': ['289490'],
        'productName': ['Exhibia'],
        'promoteContractsNum': ['0'],
        'quantity': ['1'],
        'referenceNumber': ['1002906620'],
        'remoteAddress': ['186.113.118.234'],
        'shippingAddress1': ['6626 W 93rd St'],
        'shippingCity': ['Oak Lawn'],
        'shippingCountry': ['US'],
        'shippingFirstName': ['John'],
        'shippingLastName': ['Doe'],
        'shippingState': ['ID'],
        'shippingZipCode': ['60453'],
        'state': ['ID'],
        'targetBalance': ['PLIMUS_ACCOUNT'],
        'testMode': ['N'],
        'transactionDate': ['12/08/2011 02:38 PM'],
        'transactionType': ['CHARGE'],
        'untilDate': ['12/08/2011 02:38 PM'],
        'username': ['1323383684612'],
        'workPhone': ['18583507473'],
        'zipCode': ['60453'],
        'item_number': 'PCKG10',
        'item_name': 'Credit Package 10',
        'member':'vh5'}
        member = Member.objects.get(user__username=data['member'])
        package = CreditPackage.objects.get(code=data['item_number'])
        credits = member.credits
        self.client.post('/pay/package/plimus/', data)
        member = Member.objects.get(user__username=data['member'])
        self.assertEqual(member.credits, credits)
        order = CreditPackageOrder.objects.latest('id')
        self.assertEqual(order.status, SUSPENDED)

