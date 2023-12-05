from dateutil.relativedelta import relativedelta
from django.forms import forms
from django.test import tag, TestCase
from edc_action_item import site_action_items
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import CLOSED, OPEN
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from potlako_subject.action_items import NAVIGATION_PLANS_ACTION
from potlako_subject.forms.subject_visit_form import VisitFormValidator


@tag('visit_form')
class TestValidateNavigationActionRequired(TestCase):

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
        self.appointment = Appointment.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier).first()
        self.subject_identifier = self.appointment.subject_identifier
        self.action_cls = site_action_items.get(NAVIGATION_PLANS_ACTION)
        action_item_model_cls = self.action_cls.action_item_model_cls()
        self.action_cls(subject_identifier=self.subject_identifier)
        action_item_model_cls = self.action_cls.action_item_model_cls()
        self.nav_action = action_item_model_cls.objects.get(
            subject_identifier=self.subject_identifier,
            action_type__name=NAVIGATION_PLANS_ACTION)
        self.cleaned_data = {'appointment': self.appointment}

    def test_validate_navigation_action_required_without_action(self):
        """Test that validation error is not raised when there are no navigation plans
        action items."""
        self.nav_action.status = CLOSED
        self.nav_action.save()

        try:
            VisitFormValidator(
                cleaned_data=self.cleaned_data).validate_navigation_action_required()
        except forms.ValidationError:
            self.fail("forms.ValidationError raised unexpectedly!")

    def test_validate_navigation_action_required_with_action(self):
        """Test that validation error is raised when there are navigation plans action
        items."""
        self.nav_action.status = OPEN
        self.nav_action.save()
        with self.assertRaises(forms.ValidationError):
            VisitFormValidator(
                cleaned_data=self.cleaned_data).validate_navigation_action_required()
