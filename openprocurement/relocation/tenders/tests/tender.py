# -*- coding: utf-8 -*-
import unittest
import random

from openprocurement.relocation.core.tests.mixins import OwnershipChangeTestMixin
from openprocurement.relocation.tenders.tests.base import (
    OwnershipWebTest,
    OpenUAOwnershipWebTest,
    OpenEUOwnershipWebTest,
    test_tender_data,
    test_ua_tender_data,
    test_uadefense_tender_data,
    test_eu_tender_data,
    test_tender_reporting_data,
    test_tender_negotiation_data,
    test_tender_negotiation_quick_data
)


class TenderOwnershipChangeTest(OwnershipWebTest, OwnershipChangeTestMixin):
    initial_tender_data = test_tender_data
    first_owner = 'broker'
    second_owner = 'broker1'
    test_owner = 'broker1t'
    invalid_owner = 'broker3'
    initial_auth = ('Basic', (first_owner, ''))

    def prepare_ownership_change(self):
        self.initial_data =  self.initial_tender_data
        self.transfer = self.tender_transfer
        self.first_owner_token = self.tender_token
        self.request_path = '/{}/{}'.format(self.resource, self.tender_id)

    def check_permission(self, path, token):
        return self.app.patch_json('{}?acc_token={}'.format(path, token),
            {"data": {'description': "Check permission {}".format(random.random())}}, status="*")


class OpenUATenderOwnershipChangeTest(OpenUAOwnershipWebTest, TenderOwnershipChangeTest):
    initial_tender_data = test_ua_tender_data
    second_owner = 'broker3'
    test_owner = 'broker3t'
    invalid_owner = 'broker1'


class OpenUADefenseTenderOwnershipChangeTest(OpenUATenderOwnershipChangeTest):
    initial_tender_data = test_uadefense_tender_data


class OpenEUTenderOwnershipChangeTest(OpenEUOwnershipWebTest, OpenUATenderOwnershipChangeTest):
    initial_tender_data = test_eu_tender_data


class ReportingTenderOwnershipChangeTest(TenderOwnershipChangeTest):
    initial_tender_data = test_tender_reporting_data
    second_owner = 'broker1'
    test_owner = 'broker1t'
    invalid_owner = 'broker2'


class NegotiationTenderOwnershipChangeTest(TenderOwnershipChangeTest):
    initial_tender_data = test_tender_negotiation_data
    second_owner = 'broker3'
    test_owner = 'broker3t'
    invalid_owner = 'broker1'


class NegotiationQuickTenderOwnershipChangeTest(NegotiationTenderOwnershipChangeTest):
    initial_tender_data = test_tender_negotiation_quick_data


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderOwnershipChangeTest))
    suite.addTest(unittest.makeSuite(OpenUATenderOwnershipChangeTest))
    suite.addTest(unittest.makeSuite(OpenUADefenseTenderOwnershipChangeTest))
    suite.addTest(unittest.makeSuite(OpenEUTenderOwnershipChangeTest))
    suite.addTest(unittest.makeSuite(ReportingTenderOwnershipChangeTest))
    suite.addTest(unittest.makeSuite(NegotiationTenderOwnershipChangeTest))
    suite.addTest(unittest.makeSuite(NegotiationQuickTenderOwnershipChangeTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
