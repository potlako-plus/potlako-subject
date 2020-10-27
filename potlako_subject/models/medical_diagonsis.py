from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN

from ..choices import DATE_ESTIMATION, MEDICAL_CONDITION, CHECKUP_FREQUENCY
from .model_mixins import CrfModelMixin


class MedicalDiagnosis(CrfModelMixin):

    pass

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Medical Diagnosis'
        verbose_name_plural = 'Medical Diagnoses'


class MedicalConditions(BaseUuidModel):

    medical_diagnosis = models.ForeignKey(MedicalDiagnosis, on_delete=PROTECT)

    medical_condition = models.CharField(
        verbose_name='Which serious medical condition(s) does the patient have?',
        choices=MEDICAL_CONDITION,
        max_length=30)

    medical_condition_specify = models.CharField(
        verbose_name='Specific condition of the body area that has been affected',
        max_length=35)

    medical_condition_other = OtherCharField()

    diagnosis_date = models.DateField(
        verbose_name='When was the patient diagnosed?',
        validators=[date_not_future],
        max_length=40)

    diagnosis_date_estimate = models.CharField(
        verbose_name='Is the diagnosis date an estimate?',
        choices=YES_NO,
        max_length=3)

    diagnosis_date_estimation = models.CharField(
        verbose_name=('If diagnoses date was estimated, which part of the '
                      'date was estimated?'),
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True)

    on_medication = models.CharField(
        verbose_name='Is the patient of medication?',
        choices=YES_NO_UNKNOWN,
        max_length=7)

    treatment_type = models.CharField(
        verbose_name=('how often does the participant see a doctor/nurse for '
                      'their condition?'),
        choices=CHECKUP_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    class Meta:
        unique_together = (
            'medical_diagnosis', 'medical_condition')
