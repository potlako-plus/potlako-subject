from django.test import TestCase
from edc_action_item.models.action_item import ActionItem
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, OPEN
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment
from dateutil.relativedelta import relativedelta
from edc_appointment.constants import INCOMPLETE_APPT



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
            'consent_datetime': get_utcnow() - relativedelta(days=2),
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

        self.maternal_visit_1000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=self.appointment_1000)

    def test_subject_locator_action_created(self):
        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            reference_model='potlako_subject.subjectlocator',
            status='New').count(), 0)
        
        self.appointment_1000.appt_status = INCOMPLETE_APPT
        self.appointment_1000.save()
         
        self.maternal_visit_2000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=self.appointment_2000)
         
        mommy.make_recipe('potlako_subject.patientcallfollowup',
            subject_visit=self.maternal_visit_2000,
            patient_info_change=YES)
 
        self.assertEqual(ActionItem.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            reference_model='potlako_subject.subjectlocator',
            status=OPEN).count(), 1)
