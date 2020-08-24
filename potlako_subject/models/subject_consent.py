from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_identifier.subject_identifier import SubjectIdentifier
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)

from edc_consent.field_mixins import CitizenFieldsMixin
from edc_consent.field_mixins import IdentityFieldsMixin
from edc_consent.field_mixins import ReviewFieldsMixin, PersonalFieldsMixin
from edc_consent.managers import ConsentManager as SubjectConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_consent.validators import eligible_if_yes
from edc_search.model_mixins import SearchSlugManager
from edc_sms.models import SubjectRecipientModelMixin

from ..choices import IDENTITY_TYPE
from .clinician_call_enrollment import ClinicianCallEnrollment
from .model_mixins import SearchSlugModelMixin



class ConsentManager(SubjectConsentManager, SearchSlugManager):

    def get_by_natural_key(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)

    class Meta:
        abstract = True


class SubjectConsent(
        ConsentModelMixin, SiteModelMixin, SubjectRecipientModelMixin,
        UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin,
        IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
        CitizenFieldsMixin, SearchSlugModelMixin, BaseUuidModel):

    subject_screening_model = 'potlako_subject.subjectscreening'

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        null=True,
        blank=True,
        max_length=50)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    language = models.CharField(
        verbose_name='Language of consent',
        max_length=25,
        choices=settings.LANGUAGES,
        help_text=(
            'The language used for the consent process will '
            'also be used during data collection.')
    )

    consent_reviewed = models.CharField(
        verbose_name='I have reviewed the consent with the participant',
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        help_text='If no, participant is not eligible.')

    study_questions = models.CharField(
        verbose_name=(
            'I have answered all questions the participant had about the study'),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        help_text='If no, participant is not eligible.')

    assessment_score = models.CharField(
        verbose_name=(
            'I have asked the participant questions about this study and '
            'the participant has demonstrated understanding'),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        help_text='If no, participant is not eligible.')

    verbal_script = models.CharField(
        verbose_name=('I have documented participant\'s details on the verbal '
                      'script, and signed electronically'),
        max_length=15,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        help_text='If no, participant is not eligible.')

    consent = SubjectConsentManager()

    objects = ConsentManager()

    on_site = CurrentSiteManager()

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.subject_type = 'subject'
        self.version = '1'

    def natural_key(self):
        return (self.subject_identifier, self.version,)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['identity', 'screening_identifier',
                       'first_name', 'last_name'])
        return fields

    def make_new_identifier(self):
        """Returns a new and unique identifier.
        Override this if needed.
        """
        subject_identifier = SubjectIdentifier(
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return subject_identifier.identifier

    @property
    def recipient_number(self):
        """Return a mobile number.

        Override to return a mobile number format: 26771111111.
        """
        try:
            clinic_call_enrollment = ClinicianCallEnrollment.objects.get(
                screening_identifier=self.screening_identifier)
        except ClinicianCallEnrollment.DoesNotExist:
            raise ValidationError('Missing clinic enrollment')
        else:
            return '267' + clinic_call_enrollment.primary_cell
        return None

    @property
    def consent_version(self):
        return self.version

    class Meta(ConsentModelMixin.Meta):
        app_label = 'potlako_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created',)
