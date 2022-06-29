from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from django_q.models import Schedule
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_schedule.models import SubjectScheduleHistory
from model_mommy import mommy
from ast import literal_eval as make_tuple

from edc_appointment.models import Appointment
from ..models import OnSchedule
from edc_appointment.constants import INCOMPLETE_APPT


@tag('soc')
class TestStandardofCareVisitSchedule(TestCase):

    def setUp(self):
        import_holidays()

        clinicial_call_enrolment = self.subject_screening = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment',
            facility='bokaa_clinic')

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier=clinicial_call_enrolment.screening_identifier)

        self.options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow() - relativedelta(days=5),
            'identity': clinicial_call_enrolment.national_identity,
            'confirm_identity': clinicial_call_enrolment.national_identity,
            'version': '1'}

        mommy.make_recipe(
            'potlako_subject.verbalconsent',
            screening_identifier=self.subject_screening.screening_identifier)

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

        self.appointment_2000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2000')

        self.visit_2000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=self.appointment_2000)

        self.appointment_3000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='3000')

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=1),
            appointment=self.appointment_3000)

        self.not_required_models = [
            'transport', 'investigationsordered', 'investigationsresulted']

    def test_community_arm_name_valid(self):
        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnSchedule.objects.get(
            subject_identifier=self.subject_consent.subject_identifier).community_arm,
                         'Standard of Care')

    def test_metadata_creation_visit_1000(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallinitial',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.symptomandcareseekingassessment',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.medicaldiagnosis',
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
                model='potlako_subject.cancerdxandtx',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_followup_not_required(self):

        self.appointment_1000.appt_stat = INCOMPLETE_APPT

        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.visit_2000,
            investigations_ordered='ordered_and_resulted')

        self.assertEqual(
            Appointment.objects.filter(
                subject_identifier=self.subject_consent.subject_identifier).count(), 3)

    def test_metadata_creation_visit_3000(self):

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallfollowup',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3000').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.cancerdxandtx',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3000').entry_status, REQUIRED)

    def test_models_not_required(self):
        visit_codes = ['1000', '2000', '3000']
        for code in visit_codes:
            for md in self.not_required_models:
                self.assertEqual(
                    CrfMetadata.objects.get(
                        model='potlako_subject.' + md,
                        subject_identifier=self.subject_consent.subject_identifier,
                        visit_code=code).entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.missedvisit',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2000').entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.missedvisit',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3000').entry_status, NOT_REQUIRED)

    def test_appointments_created(self):
        """Assert that four appointments were created"""

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 3)

    @tag('soc1')
    def test_schedule_history_object_created(self):
        """Assert that four appointments were created"""

        self.assertEqual(SubjectScheduleHistory.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

    def test_sms_not_set(self):
        """
        Test if an appointment has not been scheduled for participant in soc communities
        :return: None
        """
        scheduled_sms = Schedule.objects.all()
        for index, sms in enumerate(scheduled_sms):
            if self.subject_consent.subject_identifier in make_tuple(sms.args):
                self.assertNotIn(self.subject_consent.subject_identifier,
                                 make_tuple(sms.args))
