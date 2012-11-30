# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase

class ProvileViewsTest(TestCase):
    fixtures = ['dev.json']

    def test_manage_payments(self):
        self.client.login(username='krya', password=666)
        res = self.client.get(reverse('member_info'))
        self.assertEqual(res.status_code, 200)


