from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import INCOMPLETE
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_appointment.models import Appointment
from ..models import OnscheduleIntervention


class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        clinicial_call_enrolment = self.subject_screening = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment')

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier=clinicial_call_enrolment.screening_identifier)

        self.options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow() - relativedelta(days=5),
            'version': '1'}

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            **self.options)

        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')

        self.visit_1000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=self.appointment_1000)

        self.appointment_1010 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1010')

        self.visit_1010 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=4),
            appointment=self.appointment_1010)

        self.appointment_2000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2000')

        self.appointment_2010 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2010')

        self.appointment_3000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='3000')

        self.appointment_3010 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='3010')

    def test_schedule_name_valid(self):
        self.assertEqual(OnscheduleIntervention.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(self.visit_1000.schedule_name, 'intervention_schedule')

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

    def test_metadata_creation_visit_1010(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallfollowup',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1010').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1010').entry_status, NOT_REQUIRED)

    def test_creation_of_1010_continuation_visit(self):
        self.appointment_1000.appt_status = INCOMPLETE
        self.appointment_1000.save_base(raw=True)

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.visit_1010)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 7)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code=1010).count(), 2)

    def test_metadata_creation_visit_2000(self):

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=self.appointment_2000)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.cancerdiagnosisandtreatmentassessment',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_metadata_creation_visit_2010(self):

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=self.appointment_2000)

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_2010)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallfollowup',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2010').entry_status, REQUIRED)

    def test_metadata_creation_visit_3000(self):
        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=self.appointment_2000)

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_2010)

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_3000)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.cancerdiagnosisandtreatmentassessment',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3000').entry_status, REQUIRED)

    def test_metadata_creation_visit_3010(self):
        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=self.appointment_2000)

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_2010)

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_3000)

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_3010)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallfollowup',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3010').entry_status, REQUIRED)

    def test_appointments_created(self):
        """Assert that four appointments were created"""

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 6)
