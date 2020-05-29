from datetime import datetime

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item.site_action_items import site_action_items
from edc_appointment.constants import NEW_APPT
from edc_appointment.creators import AppointmentInProgressError
from edc_appointment.creators import InvalidParentAppointmentMissingVisitError
from edc_appointment.creators import InvalidParentAppointmentStatusError
from edc_appointment.creators import UnscheduledAppointmentCreator
from edc_appointment.creators import UnscheduledAppointmentError
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
import pytz

from ..action_items import TRANSPORT_ACTION, INVESTIGATIONS_ACTION
from .clinician_call_followup import ClinicianCallFollowUp
from .missed_visit import MissedVisit
from .patient_call_followup import PatientCallFollowUp
from .patient_call_initial import PatientCallInitial
from .subject_consent import SubjectConsent
from .subject_screening import SubjectScreening


# from potlako_dashboard.patterns import subject_identifier
# from .subject_locator import SubjectLocator
@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Update subject screening consented flag.
    """
    if not raw:
        if not created:
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                'potlako_subject.onschedule')
            schedule.refresh_schedule(
                subject_identifier=instance.subject_identifier)
        else:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier)
            subject_screening.subject_identifier = instance.subject_identifier
            subject_screening.is_consented = True
            subject_screening.save_base(
                update_fields=['subject_identifier', 'is_consented'])

            # put subject on schedule
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                'potlako_subject.onschedule')
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.consent_datetime)


@receiver(post_save, weak=False, sender=ClinicianCallFollowUp,
          dispatch_uid='clinician_call_followup_on_post_save')
def clinician_call_followup_on_post_save(sender, instance, raw, created, **kwargs):
    """Generate transport form action item.
    """

    if not raw:

        if instance.transport_support == YES:
            transport_cls = django_apps.get_model(
                'potlako_subject.transport')
            trigger_crf_action_item(transport_cls,
                                    instance.subject_visit,
                                    TRANSPORT_ACTION)

        if instance.investigation_ordered == YES:
            investigations_cls = django_apps.get_model(
                'potlako_subject.investigations')
            trigger_crf_action_item(investigations_cls,
                                    instance.subject_visit,
                                    INVESTIGATIONS_ACTION)


@receiver(post_save, weak=False, sender=MissedVisit,
          dispatch_uid='missed_visit_on_post_save')
def missed_visit_on_post_save(sender, instance, raw, created, **kwargs):
    """Generate transport form action item.
    """

    if not raw:

        if instance.transport_support == YES:
            transport_cls = django_apps.get_model(
                'potlako_subject.transport')
            trigger_crf_action_item(transport_cls,
                                    instance.subject_visit,
                                    TRANSPORT_ACTION)


@receiver(post_save, weak=False, sender=PatientCallInitial,
          dispatch_uid='patient_call_initial_on_post_save')
def patient_call_initial_on_post_save(sender, instance, raw, created, **kwargs):
    """Update appointment date and generate transport form action item.
    """

    if not raw:

        next_app = instance.next_appointment_date
        timepoint_datetime = datetime.combine(next_app, get_utcnow().time())

        try:
            appt_obj = Appointment.objects.get(
                subject_identifier=instance.subject_visit.appointment.subject_identifier,
                visit_code=instance.subject_visit.visit_code,
                visit_code_sequence=instance.subject_visit.visit_code_sequence)
        except Appointment.DoesNotExist:
            raise ValidationError(
                f'Appointment for {instance.subject_visit.appointment.subject_identifier},'
                f'visit=instance.subject_visit.visit_code '
                f'sequence={instance.subject_visit.visit_code_sequence} '
                'does not exist.')
        else:

            if appt_obj.appt_datetime != timepoint_datetime:
                appt_obj.appt_datetime = timepoint_datetime
                appt_obj.save()

        if instance.transport_support == YES:
            transport_cls = django_apps.get_model(
                'potlako_subject.transport')
            trigger_crf_action_item(transport_cls,
                                    instance.subject_visit,
                                    TRANSPORT_ACTION)


@receiver(post_save, weak=False, sender=PatientCallFollowUp,
          dispatch_uid='patient_call_followup_on_post_save')
def patient_call_followup_on_post_save(sender, instance, raw, created, **kwargs):
    """Update appointment date and generate transport form action item.
    """

    if not raw:
        next_app = instance.next_appointment_date
        timepoint_datetime = datetime.combine(next_app, get_utcnow().time())
        timepoint_datetime = pytz.utc.localize(timepoint_datetime)
        subject_visit = instance.subject_visit

        unscheduled_appointment_cls = UnscheduledAppointmentCreator
        options = {
            'timepoint_datetime': timepoint_datetime,
            'subject_identifier': subject_visit.subject_identifier,
            'visit_schedule_name': subject_visit.visit_schedule.name,
            'schedule_name': subject_visit.schedule.name,
            'suggested_datetime': timepoint_datetime,
            'visit_code': subject_visit.visit_code,
            'appt_status': NEW_APPT,
            'check_appointment': False}

        try:
            appt = Appointment.objects.get(
                appt_datetime=timepoint_datetime,
                subject_identifier=subject_visit.subject_identifier,
                visit_schedule_name=subject_visit.visit_schedule.name,
                schedule_name=subject_visit.schedule.name,
                visit_code=subject_visit.visit_code)
        except Appointment.DoesNotExist:
            try:
                unscheduled_appointment_cls(
                    **options)
            except (ObjectDoesNotExist, UnscheduledAppointmentError,
                    InvalidParentAppointmentMissingVisitError,
                    InvalidParentAppointmentStatusError,
                    AppointmentInProgressError) as e:
                raise ValidationError(str(e))
        else:
            if appt.appt_datetime != timepoint_datetime:
                appt.appt_datetime = timepoint_datetime
                appt.save()

        if instance.transport_support == YES:
            transport_cls = django_apps.get_model(
                'potlako_subject.transport')
            trigger_crf_action_item(transport_cls,
                                    instance.subject_visit,
                                    TRANSPORT_ACTION)

        if instance.investigation_ordered == YES:
            investigations_cls = django_apps.get_model(
                'potlako_subject.investigations')
            trigger_crf_action_item(investigations_cls,
                                    instance.subject_visit,
                                    INVESTIGATIONS_ACTION)


def trigger_crf_action_item(crf_cls, subject_visit, action_name):

    try:
        crf_cls.objects.get(subject_visit=subject_visit)
    except crf_cls.DoesNotExist:
        action_cls = site_action_items.get(
            crf_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=subject_visit.appointment.subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            action_cls = site_action_items.get(action_name)
            action_cls(
                subject_identifier=subject_visit.appointment.subject_identifier)
