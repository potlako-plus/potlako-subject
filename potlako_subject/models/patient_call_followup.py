from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import CellNumber
from edc_base.model_validators import date_not_future
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from ..choices import DELAYED_REASON, DISPOSITION, DISTRICT, FACILITY
from ..choices import HEALTH_FACTOR, PATIENT_FACTOR
from .list_models import CallAchievements
from .model_mixins import ModelCsvFormExportMixin


class PatientCallFollowUp(BaseUuidModel):

    model_csv_form_export = ModelCsvFormExportMixin

    coordinator_encounter_date = models.DateField(
        verbose_name='Date of coordinator encounter',
        validators=[date_not_future])

    start_time = models.TimeField(
        verbose_name='Patient follow up: start time',
    )

    encounter_duration = models.DurationField(
        verbose_name='Duration of encounter',
        help_text='Minutes'
    )

    patient_residence_change = models.CharField(
        verbose_name=('Has their been any change in patient '
                      'residence information?'),
        choices=YES_NO,
        max_length=3)

    patient_district = models.CharField(
        verbose_name='Patient residence (district)',
        choices=DISTRICT,
        max_length=50)

    patient_village = models.CharField(
        verbose_name='Patient residence (village)',
        max_length=50)

    patient_kgotla = models.CharField(
        verbose_name='Patient residence (kgotla)',
        max_length=50)

    phone_number_change = models.CharField(
        verbose_name=('Has their been any change in patient phone number?'),
        choices=YES_NO,
        max_length=3)

    patient_number = EncryptedCharField(
        verbose_name='Please enter updated patient phone number',
        max_length=8,
        validators=[CellNumber, ],)

    next_kin_contact_change = models.CharField(
        verbose_name=('Any changes to be made to next of kin contact '
                      'information (patient phone)?'),
        choices=YES_NO,
        max_length=3)

    primary_keen_contact = EncryptedCharField(
        verbose_name='Please enter next of kin 1 phone number',
        max_length=8,
        validators=[CellNumber, ])

    secondary_keen_contact = EncryptedCharField(
        verbose_name='Please enter next of kin 2 phone number',
        max_length=8,
        validators=[CellNumber, ])

    perfomance_status = models.IntegerField(
        verbose_name='Patient performance status',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    pain_score = models.IntegerField(
        verbose_name='Patient pain score',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    new_complaints = models.CharField(
        verbose_name=('Does the patient have any new complaints?'),
        choices=YES_NO,
        max_length=3)

    new_complaints_description = models.TextField(
        verbose_name=('If yes, please describe'),
        max_length=100,
        blank=True,
        null=True)

    interval_visit = models.CharField(
        verbose_name=('Have there been any interval visits to facilities '
                      'since the enrollment visit?'),
        choices=YES_NO,
        max_length=3,
        help_text=('If yes, details should be verified with clinician at next '
                   'clinician check-in call and reconciled with clinician '
                   'call encounter records'))

    interval_visit_date = models.DateField(
        verbose_name='Date of interval visit',
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True)

    visit_facility = models.CharField(
        verbose_name=('What facility was visited (per patient report)?'),
        choices=FACILITY,
        max_length=30,
        null=True,
        blank=True)

    visit_reason = models.CharField(
        verbose_name=('What was the reason for the visit?'),
        max_length=50,
        null=True,
        blank=True)

    visit_outcome = models.CharField(
        verbose_name='What was the outcome of the visit?',
        choices=DISPOSITION,
        max_length=15,
        blank=True,
        null=True)

    investigation_ordered = models.CharField(
        verbose_name=('Have there been any interval investigations '
                      'ordered or resulted?'),
        choices=YES_NO,
        max_length=3,
        help_text='(IF YES, COMPLETE \'INVESTIGATION FORM\')')

    transport_support = models.CharField(
        verbose_name=('Does the patient need transport support?'),
        choices=YES_NO,
        max_length=3,
        help_text='(IF YES, COMPLETE \'TRANSPORT FORM\')')

    next_appointment_date = models.DateField(
        verbose_name='Next appointment date (per patient report)')

    next_visit_delayed = models.CharField(
        verbose_name=('Was the next visit date delayed, missed or '
                      'rescheduled for this encounter?'),
        choices=YES_NO,
        max_length=3)

    visit_delayed_count = models.IntegerField(
        verbose_name='If yes, how many times?',
        blank=True,
        null=True)

    visit_delayed_reason = models.CharField(
        verbose_name=('If yes, was delayed, missed, or rescheduled '
                      'visit primarily related to a patient or '
                      'health system factor?'),
        choices=DELAYED_REASON,
        max_length=25,
        null=True,
        blank=True)

    patient_factor = models.CharField(
        verbose_name=('Which patient factor best describes reason for '
                      'delayed, missed, or rescheduled visit?'),
        choices=PATIENT_FACTOR,
        max_length=50,
        null=True,
        blank=True)

    patient_factor_other = OtherCharField(
        verbose_name='Please describe other patient factor',
        max_length=50,
        blank=True,
        null=True)

    health_system_factor = models.CharField(
        verbose_name=('Which health system factor best describes reason '
                      'for delayed, missed, or rescheduled visit?'),
        choices=HEALTH_FACTOR,
        max_length=50,
        null=True,
        blank=True)

    health_system_factor_other = OtherCharField(
        verbose_name='Please describe other health system factor',
        max_length=50,
        blank=True,
        null=True)

    delayed_visit_description = models.TextField(
        verbose_name=('Please briefly describe the situation resulting in '
                      'the delayed, missed, or rescheduled visit'),
        max_length=150,
        blank=True,
        null=True)

    next_appointment_facility = models.CharField(
        verbose_name='Next appointment facility and type',
        choices=FACILITY,
        max_length=30)

    patient_understanding = models.CharField(
        verbose_name=('Is patient\'s understanding of the next appointment '
                      '(date and location) the same as clinicians?'),
        choices=YES_NO,
        max_length=3,
        help_text=('If not, inform patient of the date as specified by the '
                   'clinician. If there is a discrepancy, call clinician '
                   'to verify'))

    transport_support_received = models.CharField(
        verbose_name=('Did patient receive expected transportation support '
                      'for his/her last visit?'),
        choices=YES_NO,
        max_length=3,
        help_text='e.g. funds transferred, vehicle arrived, etc.')

    transport_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    clinician_communication_issues = models.CharField(
        verbose_name=('Have there been any issues in communication with '
                      'clinicians, or with their care in general?'),
        choices=YES_NO,
        max_length=3)

    clinician_issues_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    coordinator_communication_issues = models.CharField(
        verbose_name=('Have there been any issues in communication with '
                      'coordinator?'),
        choices=YES_NO,
        max_length=3)

    coordinator_issues_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    other_issues = models.CharField(
        verbose_name='Have there been any other issues?',
        choices=YES_NO,
        max_length=3)

    other_issues_details = models.TextField(
        verbose_name=('Please provide details'),
        max_length=100,
        blank=True,
        null=True)

    call_achievements = models.ManyToManyField(
        CallAchievements,
        verbose_name='What has been achieved during the call')

    medical_evaluation_understanding = models.CharField(
        verbose_name=('Does patient have fair understanding of next '
                      'steps regarding medical evaluation?'),
        choices=YES_NO,
        max_length=3)

    next_step_understanding = models.TextField(
        verbose_name=('Does patient have fair understanding of next '
                      'steps (details)'),
        max_length=100,
        blank=True,
        null=True)

    sms_received = models.CharField(
        verbose_name=('Did patient receive SMS reminder for last scheduled '
                      'visit?'),
        choices=YES_NO,
        max_length=3)

    additional_comments = models.TextField(
        verbose_name='Provide any additional comments',
        max_length=100,
        blank=True,
        null=True)

    patient_followup_end_time = models.TimeField(
        verbose_name='Patient follow up: end time',
    )

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Patient call - FollowUp'
