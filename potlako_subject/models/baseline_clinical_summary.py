from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_identifier.managers import SubjectIdentifierManager

from ..choices import CANCER_DIAGNOSIS, SEVERITY_LEVEL


class BaselineClinicalSummary(UniqueSubjectIdentifierFieldMixin,
                              SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_before_study_start,
                    datetime_not_future],
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    symptoms_summary = models.TextField(
        verbose_name=('Summary of presenting symptoms and clinical impression'),
        max_length=1000)

    cancer_concern = models.CharField(
        verbose_name='Cancer of greatest concern',
        choices=CANCER_DIAGNOSIS,
        max_length=20)

    cancer_concern_other = OtherCharField()

    cancer_probability = models.CharField(
        choices=SEVERITY_LEVEL,
        max_length=8)

    team_discussion = models.CharField(
        verbose_name=('Does patient require team discussion?'),
        choices=YES_NO,
        max_length=8)

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Baseline Clinical Summary'
        verbose_name_plural = 'Baseline Clinical Summaries'
