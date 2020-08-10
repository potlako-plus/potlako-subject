from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_appointment.models import Appointment


@tag('ap')
class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening')

        self.options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'version': '1'}

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            **self.options)

        appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=appointment_1000)

        appointment_2000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2000')

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=2),
            appointment=appointment_2000)

        appointment_3000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='3000')

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=appointment_3000)

        appointment_4000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='4000')

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=appointment_4000)

    def test_appointments_created(self):
        """Assert that four appointments were created"""

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 4)

    def test_metadata_creation_visit_1000(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallinitial',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, NOT_REQUIRED)

    def test_metadata_creation_visit_2000(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallfollowup',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2000').entry_status, NOT_REQUIRED)

    def test_metadata_creation_visit_3000(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.cancerdiagnosisandtreatmentassessment',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3000').entry_status, REQUIRED)

    def test_metadata_creation_visit_4000(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.cancerdiagnosisandtreatmentassessment',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='4000').entry_status, REQUIRED)
