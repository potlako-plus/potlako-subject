from django.db.models.signals import post_save
from django.dispatch import receiver

from .subject_consent import SubjectConsent
from .subject_screening import SubjectScreening


@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Update subject screening consented flag.
    """
    if not raw:
        if created:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier)
            subject_screening.subject_identifier = instance.subject_identifier
            subject_screening.is_consented = True
            subject_screening.save_base(
                update_fields=['subject_identifier', 'is_consented'])

