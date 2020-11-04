from django.db import models
from edc_base.model_mixins import BaseUuidModel
from django.utils.html import mark_safe
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager

from .model_mixins import SearchSlugModelMixin
from edc_base.utils import get_utcnow
from django.conf import settings


class EnrollmentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(
            screening_identifier=screening_identifier
        )


class VerbalConsent(
        NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
        SearchSlugModelMixin, BaseUuidModel):
    
    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        default=1)

    screening_identifier = models.CharField(
        verbose_name="Screening Identifier",
        max_length=36,
        unique=True,)
    
    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        blank=True)

    file = models.FileField(upload_to='verbal_consents/',
                            null=True,
                            blank=True)
    
    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='user uploaded',)
    
    datetime_captured = models.DateTimeField(
        default=get_utcnow,
        blank=True,
        null=True,)

    language = models.CharField(
        verbose_name='Language of consent',
        max_length=25,
        choices=settings.LANGUAGES)
    
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
