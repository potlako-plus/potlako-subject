from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject

from ..models import OnSchedule


@tag('iv')
class TestInterventionVisitScheduleSetup(TestCase):

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
            'identity': clinicial_call_enrolment.national_identity,
            'confirm_identity': clinicial_call_enrolment.national_identity,
            'version': '1'}

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            **self.options)

        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')

        self.appointment_2000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2000')

        self.appointment_3000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='3000')

        self.visit_1000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=self.appointment_1000)

        self.not_required_models = [
            'transport', 'missedvisit',
            'investigationsordered', 'investigationsresulted', ]

    def test_community_arm_name_valid(self):
        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnSchedule.objects.get(
            subject_identifier=self.subject_consent.subject_identifier).community_arm, 'Intervention')

    @tag('rsb')
    def test_registered_subject(self):
        self.assertIsNotNone(RegisteredSubject.objects.get(
            subject_identifier=self.subject_consent.subject_identifier))

        self.assertIsNotNone(RegisteredSubject.objects.get(
            identity=self.subject_consent.identity))

    def test_appointments_created(self):
        """Assert that four appointments were created"""

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 3)

    def test_metadata_creation_visit_1000(self):
        """Assert that 1000 metadata is correct"""

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.patientcallinitial',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
            ).entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.medicaldiagnosis',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000').entry_status, NOT_REQUIRED)

    def test_creation_of_1000_continuation_visit(self):
        """Assert that an unscheduled appointment was created for visit 1000"""

        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.visit_1000,
            next_appointment_date=get_utcnow().date() + relativedelta(weeks=1))

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 4)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code=1000,
            visit_code_sequence='1').count(), 1)

    @tag('ov')
    def test_creation_of_continuation_visit_overlap(self):
        """Assert that an unscheduled appointment was not created for visit 1000
        if it overlaps with 2000 visit"""

        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.visit_1000,
            next_appointment_date=(self.appointment_2000.appt_datetime.date() +
                                   relativedelta(weeks=1)))

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 3)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code=1000,
            visit_code_sequence='1').count(), 0)

    def test_second_creation_of_1000_continuation_visit(self):
        """Assert that a second unscheduled appointment was created for
         visit 1000
        """

        self.appointment_1000.appt_status = INCOMPLETE_APPT
        self.appointment_1000.save()

        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.visit_1000,
            next_appointment_date=get_utcnow().date() + relativedelta(weeks=1))

        self.appointment_1000_1 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000',
            visit_code_sequence='1')

        visit_1000_1 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=self.appointment_1000_1)

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=visit_1000_1,
            next_appointment_date=get_utcnow().date() + relativedelta(weeks=2))

        for model in self.not_required_models:
            self.assertEqual(
                CrfMetadata.objects.get(
                    model='potlako_subject.' + model,
                    subject_identifier=self.subject_consent.subject_identifier,
                    visit_code='1000',
                    visit_code_sequence='1').entry_status, NOT_REQUIRED)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 5)

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code=1000,
            visit_code_sequence='2').count(), 1)

    def test_metadata_creation_visit_2000(self):

        appts = Appointment.objects.filter(appt_status=IN_PROGRESS_APPT)

        for ap in appts:
            ap.appt_status = INCOMPLETE_APPT
            ap.save()

        mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=3),
            appointment=self.appointment_2000)

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
            appointment=self.appointment_3000)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.cancerdxandtx',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='3000').entry_status, REQUIRED)
