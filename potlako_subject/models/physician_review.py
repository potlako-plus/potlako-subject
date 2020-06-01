from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..choices import (
    CANCER_DIAGNOSIS, CANCER_EVALUATION, CANCER_STATUS, NON_CANCER_DIAGNOSIS,
    REVIEWER)
from .model_mixins import CrfModelMixin


class PhysicianReview(CrfModelMixin):

    reviewer_name = models.CharField(
        verbose_name='Name of reviewer',
        choices=REVIEWER,
        max_length=5,)

    reviewer_name_other = OtherCharField(
        verbose_name='Physician reviewer (other - specify)',
        max_length=25,
        blank=True,
        null=True,)

    physician_summary = models.CharField(
        max_length=50,)

    diagnosis_plan = models.TextField(
        verbose_name='Diagnosis/Management plan',
        max_length=150,)

    needs_discussion = models.CharField(
        verbose_name='Needs management discussion',
        choices=YES_NO,
        max_length=3,)

    research_staff_summary = models.CharField(
        verbose_name='Research staff summary',
        max_length=50,)

    cancer_eval = models.CharField(
        verbose_name='Cancer evaluation',
        choices=CANCER_EVALUATION,
        max_length=50,)

    reason_fu_needed = models.CharField(
        verbose_name='Why patient needs continued Potlako+ follow-up',
        max_length=100,)

    final_status = models.CharField(
        choices=CANCER_STATUS,
        max_length=40,)

    non_cancer_diagnosis = models.CharField(
        verbose_name='Final Non-Cancer diagnosis',
        choices=NON_CANCER_DIAGNOSIS,
        max_length=40,
        blank=True,
        null=True,)

    non_cancer_diagnosis_other = OtherCharField(
        verbose_name='Final Non-Cancer Diagnosis, Other',
        max_length=40,)

    cancer_diagnosis = models.CharField(
        verbose_name='Final Cancer Diagnosis',
        choices=CANCER_DIAGNOSIS,
        max_length=30,
        blank=True,
        null=True,)

    cancer_diagnosis_other = OtherCharField(
        verbose_name='Final Cancer Diagnosis, Other',
        max_length=40,
        blank=True,
        null=True,)

    to_be_flagged = models.CharField(
        verbose_name='Case instructive and to be flagged for future reference',
        choices=YES_NO,
        max_length=3,)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Physician Review'
