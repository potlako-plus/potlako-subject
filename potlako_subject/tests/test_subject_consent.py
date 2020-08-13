import re

from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnscheduleIntervention, SubjectScreening, SubjectConsent

subject_identifier = '132\-[0-9\-]+'


class TestSubjectConsent(TestCase):

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

    def test_screening_created(self):
        """Test subject screening model created"""

        self.assertTrue(isinstance(self.subject_screening, SubjectScreening))

    def test_allocated_subject_idenfier(self):
        """Test consent successfully allocates subject identifier on
        save.
        """

        mommy.make_recipe('potlako_subject.subjectconsent', **self.options)

        self.assertTrue(
            re.match(
                subject_identifier,
                SubjectConsent.objects.all()[0].subject_identifier))

    def test_update_subject_identifier_on_screening(self):
        """Test if subject identifier on screening is updated after consent
        """

        subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent', **self.options)
        subject_screening = SubjectScreening.objects.get(
            screening_identifier=self.subject_screening.screening_identifier)
        self.assertEqual(
            subject_screening.subject_identifier,
            subject_consent.subject_identifier)

    def test_consent_creates_registered_subject(self):
        """Test if registered subject is created.
        """

        options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'version': '1'
        }

        subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent', **options)
        try:
            RegisteredSubject.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            raise ValidationError('Registered subject is expected.')
        self.assertEquals(RegisteredSubject.objects.all().count(), 1)

    def test_onschedule_created_on_consent(self):
        """Test if subject is put onschedule after successful consent"""

        subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            **self.options)

        try:
            OnscheduleIntervention.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except OnscheduleIntervention.DoesNotExist:
            raise ValidationError(
                'Onschedule object does not exist for subject')
        self.assertEqual(OnscheduleIntervention.objects.all().count(), 1)

    def test_ineligibilty_consent_validation_raised(self):
        """Test validation error raised when subject ineligible
        during consent"""

        options = self.options
        options.update(
            study_questions=YES,
            assessment_score=YES,
            consent_signature=YES,
            consent_copy=YES,
            identity_type='country_id',
            consent_reviewed=NO)

        subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent', **options)

        try:
            subject_consent.full_clean()
        except ValidationError as e:
            self.assertTrue('consent_reviewed' in e.message_dict)
