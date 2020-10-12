from django.test import TestCase
from edc_action_item.models.action_item import ActionItem
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment
from ..models import PatientCallInitial


class TestSubjectLocatorAction(TestCase):

    def setUp(self):
        import_holidays()

        clinicial_call_enrolment = self.subject_screening = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment')

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier=clinicial_call_enrolment.screening_identifier)

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

        self.appointment_2000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2000')

        self.maternal_visit_1000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appointment_1000)

    def test_subject_locator_action_created(self):
        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            reference_model='potlako_subject.subjectlocator',
            status='New').count(), 0)

        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000,
            patient_info_change=YES)

        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            reference_model='potlako_subject.subjectlocator',
            status='New').count(), 1)

    def test_subject_locator_action_recreation(self):
        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            reference_model='potlako_subject.subjectlocator',
            status='New').count(), 0)

        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.maternal_visit_1000,
            patient_info_change=YES)

        patient_initial = PatientCallInitial.objects.get(
            subject_visit=self.maternal_visit_1000)
        patient_initial.save()

        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            reference_model='potlako_subject.subjectlocator',
            status='New').count(), 1)
