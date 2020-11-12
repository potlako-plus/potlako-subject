from django.test import TestCase, tag
from edc_sync.models import OutgoingTransaction
from dateutil.relativedelta import relativedelta
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from .subject_helper_mixin import SubjectHelperMixin


@tag('ot')
class TestRuleGroups(TestCase):
    
    def test_outgoing_transactions_none_valid(self):
        self.assertEqual(
            OutgoingTransaction.objects.all().count(), 0)
        
        
    def test_outgoing_transactions_valid(self):
        import_holidays()
        
        self.subject_helper = SubjectHelperMixin()
        subject_identifier = self.subject_helper.create_enrollment(community='otse_clinic')

        
        self.subject_helper.create_visit_1000(subject_identifier=subject_identifier)
        
        self.assertNotEqual(
            OutgoingTransaction.objects.all(), 0)
