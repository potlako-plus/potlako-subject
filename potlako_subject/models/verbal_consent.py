from django.conf import settings
from django.db import models
from django.utils.html import mark_safe
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager

from ..eligibility import Eligibility
from .model_mixins import SearchSlugModelMixin


class VerbalConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(
            screening_identifier=screening_identifier
        )


class VerbalConsent(
        NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
        SearchSlugModelMixin, BaseUuidModel):

    eligibility_cls = Eligibility

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,)

    screening_identifier = models.CharField(
        verbose_name="Screening Identifier",
        max_length=36,
        unique=True,)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        blank=True)

    consented = models.CharField(
        verbose_name='Agree to Consent',
        max_length=4,
        choices=YES_NO)

    file = models.FileField(upload_to='verbal_consents/')

    user_uploaded = models.CharField(
        max_length=50,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow,)

    language = models.CharField(
        verbose_name='Language of consent',
        max_length=25,
        choices=settings.LANGUAGES)

    signature = models.CharField(
        max_length=5,)

    designation = models.CharField(
        max_length=30,)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = VerbalConsentManager()

    def save(self, *args, **kwargs):
        eligibility_obj = self.eligibility_cls(
           verbal_consent=self.consented,)
        self.is_eligible = eligibility_obj.is_eligible
        if eligibility_obj.reasons_ineligible:
            self.ineligibility = eligibility_obj.reasons_ineligible
        super().save(*args, **kwargs)

    def verbal_consent_image(self):
            return mark_safe(
                '<a href="%(url)s">'
                'Consent pdf'
                '</a>' % {'url': self.file.url})

    verbal_consent_image.short_description = 'Verbal Consent'

    verbal_consent_image.allow_tags = True

    def __str__(self):
        return f'{self.screening_identifier}, {self.subject_identifier}'

    def natural_key(self):
        return (self.screening_identifier,)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = "Potlako+ Verbal Consent"
        verbose_name_plural = "Potlako+ Verbal Consents"
