from datetime import datetime

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_action_item.site_action_items import site_action_items
from edc_base.utils import get_utcnow
from edc_constants.constants import DEAD, NEW, YES, OPEN
import pytz

from edc_appointment.constants import NEW_APPT
from edc_appointment.creators import AppointmentInProgressError
from edc_appointment.creators import InvalidParentAppointmentMissingVisitError
from edc_appointment.creators import InvalidParentAppointmentStatusError
from edc_appointment.creators import UnscheduledAppointmentCreator
from edc_appointment.creators import UnscheduledAppointmentError
from edc_appointment.models import Appointment
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from potlako_prn.action_items import DEATH_REPORT_ACTION
from potlako_prn.action_items import SUBJECT_OFFSTUDY_ACTION

from ..action_items import SUBJECT_LOCATOR_ACTION
from .cancer_dx_and_tx import CancerDxAndTx
from .clinician_call_enrollment import ClinicianCallEnrollment
from .home_visit import HomeVisit
from .missed_call import MissedCallRecord
from .onschedule import OnSchedule
from .patient_availability_log import PatientAvailabilityLog
from .patient_call_followup import PatientCallFollowUp
from .patient_call_initial import PatientCallInitial
from .subject_consent import SubjectConsent
from .subject_locator import SubjectLocator
from .subject_screening import SubjectScreening
from .subject_visit import SubjectVisit
from .verbal_consent import VerbalConsent


@receiver(post_save, weak=False, sender=ClinicianCallEnrollment,
          dispatch_uid='clinician_call_enrollment_on_post_save')
def clinician_call_enrollment_on_post_save(sender, instance, raw, created, **kwargs):
    """
    - Create Patient Availability log
    """
    if not raw:
        if created:

            try:
                PatientAvailabilityLog.objects.get(clinician_call=instance)
            except PatientAvailabilityLog.DoesNotExist:
                PatientAvailabilityLog.objects.create(clinician_call=instance)


@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """
    -Update subject screening consented flag.
    -Put participant on schedule and define community arm
    """
    if not raw:
        if created:

            update_model_fields(instance=instance,
                                model_cls=SubjectScreening,
                                fields=[['subject_identifier', instance.subject_identifier],
                                        ['is_consented', True]])

            update_model_fields(instance=instance,
                                model_cls=ClinicianCallEnrollment,
                                fields=[['subject_identifier', instance.subject_identifier], ])

            update_model_fields(instance=instance,
                                model_cls=VerbalConsent,
                                fields=[['subject_identifier', instance.subject_identifier], ])

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
                    subject_consent = SubjectConsent.objects.get(
                        subject_identifier=instance.subject_visit.subject_identifier)
                except SubjectConsent.DoesNotExist:
                    raise ValidationError('Subject consent object does not exist!')
                else:
                    if (instance.next_appointment_date and get_community_arm(
                            screening_identifier=subject_consent.screening_identifier) == 'Intervention'):

                        create_unscheduled_appointment(instance=instance)


@receiver(post_save, weak=False, sender=PatientCallFollowUp,
          dispatch_uid='patient_call_followup_on_post_save')
def patient_call_followup_on_post_save(sender, instance, raw, created, **kwargs):
    """Create next unscheduled appointment if date is provided.
    """

    if not raw:
        if instance.next_appointment_date and instance.subject_visit.visit_code != '3000':
            next_visit_code = int(instance.subject_visit.visit_code_sequence) + 1
            try:
                Appointment.objects.get(
                    subject_identifier=instance.subject_visit.subject_identifier,
                    visit_code=instance.subject_visit.visit_code,
                    visit_code_sequence=next_visit_code)
            except ObjectDoesNotExist:
                try:
                    subject_consent = SubjectConsent.objects.get(
                        subject_identifier=instance.subject_visit.subject_identifier)
                except SubjectConsent.DoesNotExist:
                    raise ValidationError('Subject screening object does not exist!')
                else:
                    if (instance.next_appointment_date and get_community_arm(
                            screening_identifier=subject_consent.screening_identifier) == 'Intervention'):
                        create_unscheduled_appointment(instance=instance)

        trigger_action_item(instance, 'patient_info_change', YES,
                            SubjectLocator, SUBJECT_LOCATOR_ACTION,
                            instance.subject_visit.appointment.subject_identifier,
                            repeat=True)


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


@receiver(post_save, weak=False, sender=MissedCallRecord,
          dispatch_uid='missed_call_on_post_save')
def missed_call_on_post_save(sender, instance, raw, created, **kwargs):
    """Run rule groups if the third record for missed call is saved.
    """
    if not raw:
        missed_call_count = MissedCallRecord.objects.filter(
            missed_call=instance.missed_call).count()
        if missed_call_count >= 3:
            instance.missed_call.subject_visit.run_metadata_rules(visit=instance.missed_call.visit)


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


@receiver(post_save, weak=False, sender=CancerDxAndTx,
          dispatch_uid='cancer_dx_and_tx_on_post_save')
def cancer_dx_and_tx_on_post_save(sender, instance, raw, created, **kwargs):
    """ Trigger subject offstudy based off of the cancer diagnosis and treatment
        outcome response.
    """
    if not raw:
        subject_offstudy_cls = django_apps.get_model(
            'potlako_prn.subjectoffstudy')

        field_responses = {'cancer_evaluation': 'unable_to_complete',
                           'cancer_treatment': YES}
        for field, response in field_responses.items():
            trigger_action_item(instance, field, response, subject_offstudy_cls,
                                SUBJECT_OFFSTUDY_ACTION,
                                instance.subject_visit.appointment.subject_identifier)


def trigger_action_item(obj, field, response, model_cls,
                        action_name, subject_identifier,
                        repeat=False):

    action_cls = site_action_items.get(
        model_cls.action_name)
    action_item_model_cls = action_cls.action_item_model_cls()

    if getattr(obj, field) == response:
        try:
            model_cls.objects.get(subject_identifier=subject_identifier)
        except model_cls.DoesNotExist:
            trigger = True
        else:
            trigger = repeat
        if trigger:
            try:
                action_item_obj = action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=action_name)
            except action_item_model_cls.DoesNotExist:
                action_cls = site_action_items.get(action_name)
                action_cls(subject_identifier=subject_identifier)
            else:
                action_item_obj.status = OPEN
                action_item_obj.save()
    else:
        try:
            action_item = action_item_model_cls.objects.get(
                Q(status=NEW) | Q(status=OPEN),
                subject_identifier=subject_identifier,
                action_type__name=action_name)
        except action_item_model_cls.DoesNotExist:
            pass
        else:
            action_item.delete()


def create_unscheduled_appointment(instance=None):

    next_app = instance.next_appointment_date
    appt_cls = django_apps.get_model('edc_appointment.appointment')
    subject_visit = instance.subject_visit

    try:
        next_visit_code = str(int(subject_visit.visit_code) + 1000)
        next_appt_obj = appt_cls.objects.filter(
            subject_identifier=instance.subject_visit.subject_identifier,
            visit_code=next_visit_code).latest('appt_datetime')
    except appt_cls.DoesNotExist:
        create_unscheduled = True
    else:
        create_unscheduled = next_appt_obj.appt_datetime.date() > next_app

    if create_unscheduled:

        timepoint_datetime = datetime.combine(next_app, get_utcnow().time())
        timepoint_datetime = pytz.utc.localize(timepoint_datetime)

        unscheduled_appointment_cls = UnscheduledAppointmentCreator

        options = {
            'subject_identifier': subject_visit.subject_identifier,
            'visit_schedule_name': subject_visit.visit_schedule.name,
            'schedule_name': subject_visit.schedule.name,
            'visit_code': subject_visit.visit_code,
            'suggested_datetime': timepoint_datetime,
            'timepoint_datetime': timepoint_datetime,
            'check_appointment': False,
            'appt_status': NEW_APPT,
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

        schedule.put_on_schedule(
            subject_identifier=instance.subject_identifier,
            onschedule_datetime=instance.consent_datetime)

        try:
            onschedule_obj = OnSchedule.objects.get(
                subject_identifier=instance.subject_identifier,
                community_arm__isnull=True)
        except OnSchedule.DoesNotExist:
            pass
        else:
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

            enhanced_care_communities = settings.COMMUNITIES.get('enhanced_care')

            intervention_communities = settings.COMMUNITIES.get('intervention')

            if clinician_enrollment_obj.facility in enhanced_care_communities:
                return 'Standard of Care'
            elif clinician_enrollment_obj.facility in intervention_communities:
                return 'Intervention'
    return None


def update_model_fields(instance=None, model_cls=None, fields=None):
    try:
        model_obj = model_cls.objects.get(
            screening_identifier=instance.screening_identifier)
    except model_cls.DoesNotExist:
        raise ValidationError(f'{model_cls} object does not exist!')
    else:
        for field, value in fields:
            setattr(model_obj, field, value)
        model_obj.save_base(update_fields=[field[0] for field in fields])
