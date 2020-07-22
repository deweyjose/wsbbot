from service.investor_service import InvestorService
from test.service.test_service_base import TestServiceBase


class TestInvestorService(TestServiceBase):
    investor_svc = InvestorService()

    def test_create_investor(self):
        investor = self.investor_svc.create_investor("i@i.com", "i")
        self.assertEqual("i@i.com", investor.email)
        self.assertEqual('investor', investor.roles[0].name)
