from django.test import TestCase
from edc_constants.constants import NO, YES

from ..eligibility import Eligibility


class TestEligibility(TestCase):

    """
    Participant age >= 30 is eligible
    """

    def test_valid_participant_eligibility(self):
        eligiblity = Eligibility(age_in_years=30, cancer_status=YES)
        self.assertTrue(eligiblity.is_eligible)

    """Participant age < 30 are in eligible"""

    def test_age_in_years_ineligibility(self):
        eligiblity = Eligibility(age_in_years=25, cancer_status=YES)
        self.assertFalse(eligiblity.is_eligible)
        self.assertIn('Younger than 30 years',
                      eligiblity.reasons_ineligible)

    """Participant not community resident are ineligible"""

    def test_age_in_years_greater_ineligibility(self):
        eligiblity = Eligibility(age_in_years=30, cancer_status=YES,
                                 residency=NO)
        self.assertFalse(eligiblity.is_eligible)
        self.assertIn('Not a community resident',
                      eligiblity.reasons_ineligible)

    """Participant who are not citizens are ineligible"""

    def test_citizenship_ineligibility(self):
        eligiblity = Eligibility(age_in_years=30, nationality=NO)
        self.assertFalse(eligiblity.is_eligible)
        self.assertIn('Not a Botswana citizen',
                      eligiblity.reasons_ineligible)

    """Participant who are not cancer suspect are ineligible"""

    def test_cancer_suspect_ineligibility(self):
        eligiblity = Eligibility(age_in_years=30, cancer_status=NO)
        self.assertFalse(eligiblity.is_eligible)
        self.assertIn('Not a cancer suspect',
                      eligiblity.reasons_ineligible)
