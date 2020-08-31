from potlako_subject.choices import DATE_ESTIMATION

from django.db import models
from edc_constants.choices import YES_NO

from ..choices import CANCER_EVALUATION
from .model_mixins import CrfModelMixin


class CancerDiagnosisAndTreatmentAssessment(CrfModelMixin):

    symptoms_summary = models.TextField(
        verbose_name=('Summary of symptoms and evaluation over the past 6 '
                      'months'),
        max_length=150)

    cancer_evaluation = models.CharField(
        max_length=30,
        choices=CANCER_EVALUATION)

    diagnosis_date = models.DateField(
        verbose_name='If complete, date of final diagnosis',
        blank=True,
        null=True)

    diagnosis_date_estimated = models.CharField(
        verbose_name='Is the diagnosis date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    diagnosis_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    cancer_treatment = models.CharField(
        verbose_name='Has patient received any treatment for cancer?',
        choices=YES_NO,
        max_length=3)

    treatment_description = models.TextField(
        verbose_name='If yes, describe treatment and dates for therapies',
        max_length=200,
        null=True,
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Cancer Diagnosis And Treatment Assessment'
