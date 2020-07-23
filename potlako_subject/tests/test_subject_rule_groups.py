from dateutil.relativedelta import relativedelta
from django.test import tag
from django.test.testcases import TestCase
from django.utils import timezone
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NEG
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_appointment.models import Appointment


@tag('rg')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.clinician_call_enrollment = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment')

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier='12345')

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            screening_identifier='12345')

#         import_holidays()

        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')

        self.maternal_visit_1000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=self.appointment_1000)

    def test_transport_form_not_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, NOT_REQUIRED)

    def test_transport_form_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000,
            transport_support=YES)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)

    def test_medical_diagnosis_form_not_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.medicaldiagnosis',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, NOT_REQUIRED)

    def test_medical_diagnosis_form_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000,
            medical_conditions=YES)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.medicaldiagnosis',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)

    def test_investigations_ordered_form_not_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, NOT_REQUIRED)

    def test_investigations_ordered_form_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000,
            tests_ordered='ordered')
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)

    def test_investigations_resulted_form_not_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsresulted',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, NOT_REQUIRED)

    def test_investigations_resulted_form_required_subject(self):
        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000,
            tests_ordered='resulted')
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsresulted',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)
