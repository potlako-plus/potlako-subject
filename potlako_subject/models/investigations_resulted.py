from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import CANCER_STAGES, DIAGNOSIS_RESULTS, TESTS_ORDERED_TYPE
from .model_mixins import CrfModelMixin


class InvestigationsResulted(CrfModelMixin):

    tests_resulted_type = models.CharField(
        verbose_name='What tests are being resulted?',
        choices=TESTS_ORDERED_TYPE,
        max_length=10)

    tests_resulted_type_other = OtherCharField()

    pathology_specimen_date = models.DateField(
        verbose_name='Date pathology specimen taken',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_nhl_date = models.DateField(
        verbose_name='Date pathology specimen received at NHL',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_result_date = models.DateField(
        verbose_name='Date pathology results reported',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_received_date = models.DateField(
        verbose_name='Date pathology results received by clinician',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_communicated_date = models.DateField(
        verbose_name='Date pathology results communicated to patient',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    imaging_tests_date = models.DateField(
        verbose_name='Date imaging test performed (completed)',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    specimen_tracking_notes = models.TextField(
        verbose_name=('Path specimen tracking notes'),
        max_length=100,
        blank=True,
        null=True)

    diagnosis_results = models.CharField(
        verbose_name='Diagnosis results (provider)',
        choices=DIAGNOSIS_RESULTS,
        max_length=20)

    diagnosis_results_other = OtherCharField()

    cancer_type = models.CharField(
        verbose_name='If cancer, type of cancer diagnosed',
        max_length=15,
        blank=True,
        null=True)

    diagnoses_made = models.CharField(
        verbose_name='If not cancer, diagnosis made',
        max_length=15,
        blank=True,
        null=True)

    cancer_stage = models.CharField(
        verbose_name='If cancer, stage of cancer',
        choices=CANCER_STAGES,
        max_length=20,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Investigations - Resulted'
        verbose_name_plural = 'Investigations - Resulted'
