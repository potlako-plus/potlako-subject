from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .subject_consent import SubjectConsent
from .subject_screening import SubjectScreening


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
