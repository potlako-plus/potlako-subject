from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from edc_base import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_visit_schedule.models import SubjectScheduleHistory
from model_mommy import mommy

from potlako_subject.models import CancerDxAndTxEndpoint, OnSchedule


@tag('ofs')
class TestOffScheduleFunctionality(TestCase):
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

    def test_off_schedule_functionality(self):
        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).count(), 1)

        self.assertEqual(SubjectScheduleHistory.objects.get(
            subject_identifier=self.subject_consent.subject_identifier
        ).offschedule_datetime, None)

        mommy.make(
            CancerDxAndTxEndpoint,
            subject_identifier=self.subject_consent.subject_identifier,
            final_deposition='exit')

        self.assertNotEquals(SubjectScheduleHistory.objects.get(
            subject_identifier=self.subject_consent.subject_identifier
        ).offschedule_datetime, None)
