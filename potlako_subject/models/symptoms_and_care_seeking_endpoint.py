from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin

from ..choices import DATE_ESTIMATION
from .model_mixins import CrfModelMixin
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_base.model_mixins import BaseUuidModel


class SymptomsEndpointManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SymptomsAndCareSeekingEndpointRecording(UniqueSubjectIdentifierFieldMixin,
                                              SiteModelMixin, BaseUuidModel):

    cancer_symptom_date = models.DateField(
        verbose_name='Date of first possible cancer symptom awareness')

    cancer_symptom_estimated = models.CharField(
        verbose_name='Is the awareness date estimated?',
        choices=YES_NO,
        max_length=3)

    cancer_symptom_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    discussion_date = models.DateField(
        verbose_name='Date of first discussion with someone')

    discussion_date_estimated = models.CharField(
        verbose_name='Is the discussion date estimated?',
        choices=YES_NO,
        max_length=3)

    discussion_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    seek_help_date = models.DateField(
        verbose_name=('Date that participant decided to seek help for possible '
                      'cancer symptom from clinic or hospital'))

    seek_help_date_estimated = models.CharField(
        verbose_name='Is the seeking help date estimated?',
        choices=YES_NO,
        max_length=3)

    seek_help_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    first_seen_date = models.DateField(
        verbose_name=('Date that participant was first seen at the clinic or '
                      'for possible cancer symptom'))

    first_seen_date_estimated = models.CharField(
        verbose_name='Is the first first seen date estimated?',
        choices=YES_NO,
        max_length=3)

    first_seen_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)
    
    history = HistoricalRecords()

    on_site = CurrentSiteManager()
    
    objects = SymptomsEndpointManager()
    
    def natural_key(self):
        return (self.subject_identifier, )
    natural_key.dependencies = ['sites.Site']

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Symptom And Care Seeking - Endpoint Recording'
