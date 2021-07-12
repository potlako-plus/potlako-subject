from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_protocol.validators import date_not_before_study_start

from ..choices import DIAGNOSIS_RESULTS
from .list_models import TestsOrderedType
from .model_mixins import CrfModelMixin


class InvestigationsResulted(CrfModelMixin):

    tests_resulted_type = models.ManyToManyField(
        TestsOrderedType,
        verbose_name='What tests are being resulted?')

    imaging_tests = models.CharField(
        verbose_name='If imaging, please specify',
        max_length=150,
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

    diagnosis_results = models.CharField(
        verbose_name='Diagnosis results (provider)',
        choices=DIAGNOSIS_RESULTS,
        max_length=20)

    diagnosis_results_other = OtherCharField()

    pathology_result_date = models.DateField(
        verbose_name='Date pathology results reported',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

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

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Investigations - Resulted'
        verbose_name_plural = 'Investigations - Resulted'
