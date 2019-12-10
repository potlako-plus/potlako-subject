from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_is_future, datetime_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start

from ..choices import CLINICIAN_TYPE, DISPOSITION, FACILITY, FACILITY_UNIT
from ..choices import TRIAGE_STATUS


class ClinicianCallFollowUp(models.Model):

    visit_date_time = models.DateTimeField(
        verbose_name='Date of Visit',
        validators=[datetime_not_before_study_start, datetime_not_future])

    facility_visited = models.CharField(
        verbose_name="Name and type  of facility visited",
        max_length=25,
        choices=FACILITY)

    call_clinician = models.CharField(
        verbose_name='Name of clinician spoken to on the phone '
                     'for the follow up call',
        max_length=50)

    call_clinician_type = models.CharField(
        verbose_name='Type of clinician spoken to on the phone',
        choices=CLINICIAN_TYPE,
        max_length=50)

    facility_unit = models.CharField(
        verbose_name='Unit at facility where patient was seen',
        choices=FACILITY_UNIT,
        max_length=25)

    facility_unit_other = OtherCharField(
        max_length=50,
        verbose_name=('if other, Describe unit at facility where '
                      'patient was seen'),
        blank=True,
        null=True)

    visit_type = models.CharField(
        verbose_name='Inpatient visit?',
        choices=YES_NO,
        max_length=3)

    perfomance_status = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    pain_score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    general_comments = models.TextField(
        max_length=150,
        verbose_name=('Any other general comments on visit (including '
                      'what was achieved during visit)'),
        blank=True,
        null=True)

    patient_disposition = models.CharField(
        verbose_name='Patient disposition at end of visit',
        choices=DISPOSITION,
        max_length=15)

    referral_date = models.DateField(
        verbose_name='Referral appointment date',
        validators=[date_is_future])

    referral_facility = models.CharField(
        verbose_name=('Name and type of facility patient being referred'
                      ' to (referral facility)'),
        choices=FACILITY_UNIT,
        max_length=25)

    referral_reason = models.CharField(
        verbose_name='If referred, reason for referral',
        max_length=50)

    referral_discussed = models.CharField(
        verbose_name='Was referral discussed with referral clinician?',
        choices=YES_NO,
        max_length=3,)

    referral_discussed_clinician = models.CharField(
        verbose_name=('Name of referral clinician discussed with '
                      '(and indicate whether nurse or doctor)'),
        max_length=25,
        help_text='(If referral clinician name is missing, please write "UNK")'
    )

    return_visit_scheduled = models.CharField(
        verbose_name=('If not discharged, does patient have return visit '
                      'appointment scheduled?'),
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    return_visit_date = models.DateField(
        verbose_name='Return visit appointment date',
        validators=[date_is_future])

    investigation_ordered = models.CharField(
        verbose_name='Was any investigation ordered during this visit?',
        choices=YES_NO,
        max_length=3,
        help_text='(IF YES, COMPLETE \'INVESTIGATION FORM\')')

    triage_status = models.CharField(
        verbose_name='What is this patient\'s triage status',
        choices=TRIAGE_STATUS,
        max_length=10)

    transport_support = models.CharField(
        verbose_name=('Does patient need or is patient '
                      'receiving transport support?'),
        choices=YES_NO,
        max_length=3,
        help_text='(IF YES, COMPLETE \'TRANSPORT FORM\')')

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Clinician Call - FollowUp'
