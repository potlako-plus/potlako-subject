from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_action_item import site_action_items
from edc_appointment.constants import COMPLETE_APPT, IN_PROGRESS_APPT
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import NEW
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from potlako_subject.action_items import NAVIGATION_PLANS_ACTION


@tag('navigation_plan')
class TestNavigationalPlanAction(TestCase):
    def setUp(self):
        import_holidays()

        self.clinicial_call_enrolment = self.subject_screening = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment',
            facility='bokaa_clinic')

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier=self.clinicial_call_enrolment.screening_identifier)

        self.verbal_consent = mommy.make_recipe(
            'potlako_subject.verbalconsent',
            screening_identifier=self.clinicial_call_enrolment.screening_identifier)

        self.options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'identity': self.clinicial_call_enrolment.national_identity,
            'confirm_identity': self.clinicial_call_enrolment.national_identity,
            'version': '1'}

        self.subject_consent = mommy.make_recipe('potlako_subject.subjectconsent',
                                                 **self.options)

    def test_navigational_plan_action(self):
        ap_1000 = Appointment.objects.get(
            visit_code='1000',
            subject_identifier=self.subject_consent.subject_identifier)
        ap_1000.appt_status = COMPLETE_APPT
        ap_1000.save()

        self.assertEqual(None, self.action_created())

        ap_2000 = Appointment.objects.get(
            visit_code='2000',
            subject_identifier=self.subject_consent.subject_identifier)
        ap_2000.appt_status = COMPLETE_APPT
        ap_2000.save()

        self.assertNotEquals(None, self.action_created())

    def action_created(self):
        navigation_plan_cls = django_apps.get_model(
            'potlako_subject.navigationsummaryandplan')
        action_cls = site_action_items.get(navigation_plan_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            return action_item_model_cls.objects.get(
                subject_identifier=self.subject_consent.subject_identifier,
                action_type__name=NAVIGATION_PLANS_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            return None
