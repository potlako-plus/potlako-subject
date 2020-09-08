from datetime import datetime
from potlako_subject.action_items import SUBJECT_LOCATOR_ACTION
from potlako_subject.models.subject_locator import SubjectLocator

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item.site_action_items import site_action_items
from edc_base.utils import get_utcnow
from edc_constants.constants import DEAD, NEW, YES
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
import pytz

from edc_appointment.creators import AppointmentInProgressError
from edc_appointment.creators import InvalidParentAppointmentMissingVisitError
from edc_appointment.creators import InvalidParentAppointmentStatusError
from edc_appointment.creators import UnscheduledAppointmentCreator
from edc_appointment.creators import UnscheduledAppointmentError
from edc_appointment.models import Appointment
from potlako_prn.action_items import DEATH_REPORT_ACTION
from potlako_prn.action_items import SUBJECT_OFFSTUDY_ACTION

from .clinician_call_enrollment import ClinicianCallEnrollment
from .home_visit import HomeVisit
from .onschedule import OnSchedule
from .patient_call_followup import PatientCallFollowUp
from .patient_call_initial import PatientCallInitial
from .subject_consent import SubjectConsent
from .subject_screening import SubjectScreening
from .subject_visit import SubjectVisit


@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    -Update subject screening consented flag.
    -Put participant on schedule and define community arm
    """
    if not raw:
        if created:

            try:
                subject_screening = SubjectScreening.objects.get(
                    screening_identifier=instance.screening_identifier)
            except SubjectScreening.DoesNotExist:
                raise ValidationError('Subject screening object does not exist!')
            else:
                subject_screening.subject_identifier = instance.subject_identifier
                subject_screening.is_consented = True
                subject_screening.save_base(
                    update_fields=['subject_identifier', 'is_consented'])

        put_on_schedule(instance=instance)


@receiver(post_save, weak=False, sender=PatientCallInitial,
          dispatch_uid='patient_call_initial_on_post_save')
def patient_call_initial_on_post_save(sender, instance, raw, created, **kwargs):
    """create an unscheduled appointment and generate transport form action item.
    """

    if not raw:

        try:
            Appointment.objects.get(
                subject_identifier=instance.subject_visit.subject_identifier,
                visit_code=instance.subject_visit.visit_code,
                visit_code_sequence='1')
        except ObjectDoesNotExist:
                try:
                    subject_screening = SubjectScreening.objects.get(
                        subject_identifier=instance.subject_visit.subject_identifier)
                except SubjectScreening.DoesNotExist:
                    raise ValidationError('Subject screening object does not exist!')
                else:
                    if (instance.next_appointment_date and get_community_arm(
                            screening_identifier=subject_screening.screening_identifier) == 'Intervention'):

                        create_unscheduled_appointment(instance=instance)

        trigger_action_item(instance, 'patient_info_change', YES,
                            SubjectLocator, SUBJECT_LOCATOR_ACTION,
                            instance.subject_visit.appointment.subject_identifier)


@receiver(post_save, weak=False, sender=PatientCallFollowUp,
          dispatch_uid='patient_call_followup_on_post_save')
def patient_call_followup_on_post_save(sender, instance, raw, created, **kwargs):
    """Create next unscheduled appointment if date is provided.
    """

    if not raw and instance.next_appointment_date:
        next_visit_code = int(instance.subject_visit.visit_code_sequence) + 1
        try:
            Appointment.objects.get(
                subject_identifier=instance.subject_visit.subject_identifier,
                visit_code=instance.subject_visit.visit_code,
                visit_code_sequence=str(next_visit_code))
        except ObjectDoesNotExist:
            create_unscheduled_appointment(instance=instance)


@receiver(post_save, weak=False, sender=SubjectVisit,
          dispatch_uid='subject_visit_on_post_save')
def subject_visit_on_post_save(sender, instance, raw, created, **kwargs):
    """Trigger death report action item if visit survival status is DEAD.
    """
    if not raw:
        death_report_cls = django_apps.get_model('potlako_prn.deathreport')
        trigger_action_item(instance, 'survival_status', DEAD,
                            death_report_cls, DEATH_REPORT_ACTION,
                            instance.appointment.subject_identifier)


@receiver(post_save, weak=False, sender=HomeVisit,
          dispatch_uid='home_visit_on_post_save')
def home_visit_on_post_save(sender, instance, raw, created, **kwargs):
    """trigger death report action item or subject offstudy based off
    of the home visit outcome response.
    """
    if not raw:
        death_report_cls = django_apps.get_model('potlako_prn.deathreport')
        exit_cls = django_apps.get_model('potlako_prn.coordinatorexit')
        trigger_action_item(instance, 'visit_outcome', DEAD,
                            death_report_cls, DEATH_REPORT_ACTION,
                            instance.subject_visit.appointment.subject_identifier)

        trigger_action_item(instance, 'visit_outcome', 'ltfu',
                            exit_cls, SUBJECT_OFFSTUDY_ACTION,
                            instance.subject_visit.appointment.subject_identifier)


def trigger_action_item(obj, field, response, model_cls,
                        action_name, subject_identifier):

    action_cls = site_action_items.get(
        model_cls.action_name)
    action_item_model_cls = action_cls.action_item_model_cls()

    if getattr(obj, field) == response:
        try:
            model_cls.objects.get(subject_identifier=subject_identifier)
        except model_cls.DoesNotExist:

            try:
                action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=action_name)
            except action_item_model_cls.DoesNotExist:
                action_cls = site_action_items.get(action_name)
                action_cls(
                    subject_identifier=subject_identifier)
    else:
        try:
            action_item = action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            pass
        else:
            action_item.delete()


def create_unscheduled_appointment(instance=None):

    next_app = instance.next_appointment_date
    timepoint_datetime = datetime.combine(next_app, get_utcnow().time())
    timepoint_datetime = pytz.utc.localize(timepoint_datetime)
    subject_visit = instance.subject_visit

    unscheduled_appointment_cls = UnscheduledAppointmentCreator

#     unscheduled_appointment_cls.parent_appointment =
    options = {
        'subject_identifier': subject_visit.subject_identifier,
        'visit_schedule_name': subject_visit.visit_schedule.name,
        'schedule_name': subject_visit.schedule.name,
        'visit_code': subject_visit.visit_code,
        'suggested_datetime': timepoint_datetime,
        'timepoint_datetime': timepoint_datetime,
        'check_appointment': False,
        'facility': subject_visit.appointment.facility
    }

    try:
        unscheduled_appointment_cls(**options)
    except (ObjectDoesNotExist, UnscheduledAppointmentError,
            InvalidParentAppointmentMissingVisitError,
            InvalidParentAppointmentStatusError,
            AppointmentInProgressError) as e:
        raise ValidationError(str(e))


def put_on_schedule(instance=None):
    if instance:

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            'potlako_subject.onschedule')

        community_arm = get_community_arm(instance.screening_identifier)
        try:
            onschedule_obj = OnSchedule.objects.get(
                subject_identifier=instance.subject_identifier,
                community_arm__isnull=True)
        except OnSchedule.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.consent_datetime)

            onschedule_obj = OnSchedule.objects.get(
                subject_identifier=instance.subject_identifier,
                community_arm__isnull=True)
        else:
            schedule.refresh_schedule(
                subject_identifier=instance.subject_identifier)

        onschedule_obj.community_arm = community_arm
        onschedule_obj.save()


def get_community_arm(screening_identifier=None):

    if screening_identifier:

        try:
            clinician_enrollment_obj = ClinicianCallEnrollment.objects.get(
                screening_identifier=screening_identifier)
        except ClinicianCallEnrollment.DoesNotExist:
            raise ValidationError('Clinician Call Enrollment object '
                                  'does not exist.')
        else:

            enhanced_care_communities = [
                'otse_clinic', 'mmankgodi_clinic', 'letlhakeng_clinic',
                'mathangwane clinic', 'ramokgonami_clinic', 'sefophe_clinic',
                'mmadianare_primary_hospital', 'tati_siding_clinic',
                'bokaa_clinic', 'masunga_primary_hospital', 'masunga_clinic',
                'mathangwane_clinic']

            intervention_communities = [
                'mmathethe_clinic', 'molapowabojang_clinic',
                'lentsweletau_clinic', 'oodi_clinic', 'metsimotlhabe_clinic',
                'shoshong_clinic', 'lerala_clinic', 'maunatlala_clinic',
                'nata_clinic', 'mandunyane_clinic', 'sheleketla_clinic']

            if clinician_enrollment_obj.facility in enhanced_care_communities:
                return 'Standard of Care'
            elif clinician_enrollment_obj.facility in intervention_communities:
                return 'Intervention'
    return None
