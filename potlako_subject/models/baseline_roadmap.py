from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_is_future, datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_constants.choices import YES_NO, GENDER, POS_NEG_UNKNOWN

from ..choices import PAIN_SCORE, SCALE, SEVERITY_LEVEL
from ..choices import RESULTS_PERSONNEL, SPECIALIST_CLINIC, SUSPECTED_CANCER


class BaselineRoadMap(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=timezone.now,
        validators=[datetime_not_future, ],
        help_text='Date and time of report.')

#     enrollment_datetime = models.DateTimeField(
#         verbose_name='Enrollment Time and Date',
#         default=timezone.now,
#         validators=[datetime_not_future, ])
#
#     gender = models.CharField(
#         verbose_name='Gender',
#         choices=GENDER,
#         max_length=1,)
#
#     age_in_years = models.IntegerField(
#         verbose_name='Patient age',
#         help_text='(Years)',)
#
#     hiv_status = models.CharField(
#         verbose_name=('What is patient\'s current HIV status?'),
#         choices=POS_NEG_UNKNOWN,
#         max_length=10)
#
#     patient_symptoms = models.TextField(
#         max_length=250,
#         verbose_name=('What symptom(s) is the patient having for which '
#                       'they were seen at the clinic 1 week ago?')
#     )
#
#     perfomance_status = models.IntegerField(
#         verbose_name='Patient performance status',
#         choices=SCALE,
#         validators=[MinValueValidator(0), MaxValueValidator(5)]
#     )
#
#     pain_score = models.CharField(
#         verbose_name='Patient pain score',
#         default='0_no_pain',
#         max_length=15,
#         choices=PAIN_SCORE)
#
#     suspected_cancer = models.CharField(
#         verbose_name='Suspected Cancer type',
#         max_length=30,
#         choices=SUSPECTED_CANCER,
#         help_text='(if clinician unsure, select \'unsure\')',)
#
#     suspected_cancer_other = OtherCharField(
#         verbose_name='If other suspected Cancer type, please specify',
#         max_length=30,)
#
#     suspicion_level = models.CharField(
#         verbose_name='How strong is clinician\'s suspicion for cancer?',
#         choices=SEVERITY_LEVEL,
#         max_length=10,)

    investigations_turnaround_time = models.DateField(
        verbose_name='What is the investigations turn-around time?',
        validators=[date_is_future, ])

    specialty_clinic = models.CharField(
        verbose_name='Does the patient need a specialty clinic?',
        max_length=3,
        choices=YES_NO)

    specialist_clinic_type = models.CharField(
        verbose_name='If yes, which specialist clinic?',
        max_length=15,
        choices=SPECIALIST_CLINIC,
        blank=True,
        null=True,)

    specialist_clinic_type_other = OtherCharField()

    specialist_turnaround_time = models.DateField(
        verbose_name='What is the specialist clinic turn-around time?',
        validators=[date_is_future, ],
        blank=True,
        null=True,)

    results_review_personnel = models.CharField(
        verbose_name=('Who is responsible for next patient\'s appointment'
                      '/results review?'),
        max_length=10,
        choices=RESULTS_PERSONNEL)

    results_review_personnel_other = OtherCharField()

    review_turnaround_time = models.DateField(
        verbose_name='What is the results review turn-around time?',
        validators=[date_is_future, ])

    oncology_visit = models.DateField(
        verbose_name='When is the expected oncology visit?',
        validators=[date_is_future, ])

    oncology_turnaround_time = models.DateField(
        verbose_name='What is the oncology visit turn-around time?',
        validators=[date_is_future, ])

    treatment_initiation_visit = models.DateField(
        verbose_name='When is the expected treatment initiation visit?',
        validators=[date_is_future, ])

    treatment_initiation_turnaround_time = models.DateField(
        verbose_name='What is the treatment initiation visit turn-around time?',
        validators=[date_is_future, ])

