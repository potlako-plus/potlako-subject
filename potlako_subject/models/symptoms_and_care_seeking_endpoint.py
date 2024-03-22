from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_constants.choices import YES_NO, YES_NO_UNSURE
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_identifier.managers import SubjectIdentifierManager

from ..choices import DATE_ESTIMATION
from .model_mixins import CrfModelMixin
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_base.model_mixins import BaseUuidModel


class SymptomsAndCareSeekingEndpoint(UniqueSubjectIdentifierFieldMixin,
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
        verbose_name='Date of first discussion with someone',
        null=True,
        blank=True)

    discussion_date_estimated = models.CharField(
        verbose_name='Is the discussion date estimated?',
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True)

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

    initial_symptom = models.TextField()

    symptoms_discussion = models.CharField(
        verbose_name=('Did the patient discuss their symptom with anyone?'),
        choices=YES_NO_UNSURE,
        max_length=8)

    seek_help_decision = models.TextField(
        verbose_name='Decision to seek help')

    clinic_1st_visit = models.TextField(verbose_name='First clinic visit')

    comments = models.TextField(
        verbose_name="Any comment for care seeking form",
        blank=False,
        null=False)

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    def natural_key(self):
        return (self.subject_identifier, )
    natural_key.dependencies = ['sites.Site']

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Care Seeking Endpoint'
        verbose_name_plural = 'Symptom And Care Seeking - Endpoint Recording'
