from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import CellNumber, datetime_not_future
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import datetime_not_before_study_start

from ..choices import DELAYED_REASON, PATIENT_FACTOR
from ..choices import DISTRICT, FACILITY, POS_NEG_UNKNOWN_MISSING, TEST_TYPE


class PatientCallInitial(models.Model):

    patient_call_date_time = models.DateTimeField(
        verbose_name='Date of Visit',
        validators=[datetime_not_before_study_start, datetime_not_future])

    start_time = models.IntegerField(
        verbose_name='Time at START of encounter',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(60)]
    )

    dob_known = models.CharField(
        verbose_name='Does the patient know their date of birth?',
        choices=YES_NO,
        max_length=3,)

    dob = models.DateTimeField(
        verbose_name='If yes, please enter date of birth',
        validators=[datetime_not_future],
        blank=True,
        null=True)

    patient_contact_residence_change = models.CharField(
        verbose_name=('Has there been any change in patient contact '
                      'or residence information since the initial visit '
                      'to health facility?'),
        choices=YES_NO,
        max_length=3)

    residential_district = models.CharField(
        verbose_name='Enter the updated patient residential district',
        choices=DISTRICT,
        max_length=50,
        blank=True,
        null=True)

    patient_village = models.CharField(
        verbose_name='Enter the updated patient village or town',
        max_length=30,
        blank=True,
        null=True)

    patient_kgotla = models.CharField(
        verbose_name='Enter the updated patient kgotla',
        max_length=30,
        blank=True,
        null=True)

    primary_clinic = models.CharField(
        verbose_name=('Nearest primary clinic or health post '
                      'to where patient resides'),
        choices=FACILITY,
        max_length=30)

    patient_contact_change = models.CharField(
        verbose_name=('Any changes to be made to patient contact '
                      'information (patient phone)?'),
        choices=YES_NO,
        max_length=3)

    patient_number = EncryptedCharField(
        verbose_name='Please enter updated patient phone number',
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

    next_of_kin = models.CharField(
        verbose_name='Does the patient agree to us contacting next of kin?',
        choices=YES_NO,
        max_length=3)

    next_kin_contact_change = models.CharField(
        verbose_name=('Any changes to be made to next of kin contact '
                      'information (patient phone)?'),
        choices=YES_NO,
        max_length=3)

    next_keen_number_first = EncryptedCharField(
        verbose_name='Please enter next of kin 1 phone number',
        max_length=8,
        validators=[CellNumber, ])

    next_keen_number_second = EncryptedCharField(
        verbose_name='Please enter next of kin 2 phone number',
        max_length=8,
        validators=[CellNumber, ])

    patient_symptoms = models.TextField(
        max_length=250,
        verbose_name=('What symptom(s) is the patient having for which '
                      'they were seen at the clinic 1 week ago?')
    )

    patient_symptoms_date = models.DateField(
        verbose_name=('When did the patient start experiencing symptoms?'),
        validators=[date_not_future, ])

    other_facility = models.CharField(
        verbose_name=('Before enrollment visit, has the patient been '
                      'seen for similar symptoms at other facilities?'),
        choices=YES_NO,
        max_length=3)

    facility_number = models.IntegerField(
        verbose_name='How many facilities?',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    facility_previously_visited = models.CharField(
        verbose_name=('Which facilities has the patient '
                      'been seen for similar symptoms?'),
        max_length=25,
        choices=FACILITY)

    previous_facility_period = models.CharField(
        verbose_name=('For how long was he/she seen at facilities '
                      'before enrollment visit?'),
        help_text='specify variable (days, weeks, months, years)')

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

    hiv_status = models.CharField(
        verbose_name=('What is patient\'s current HIV status?'),
        choices=POS_NEG_UNKNOWN_MISSING,
        max_length=10)

    hiv_test_date_known = models.CharField(
        verbose_name=('If positive or negative, does patient know '
                      'date of Yes last HIV test?'),
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    hiv_test_date = models.DateField(
        verbose_name=('If patient knows date of last HIV test, please record'),
        validators=[date_not_future, ],
        help_text=('If positive test, date of positive test, if negative, '
                   'date of most recent negative test'))

    cancer_suspicion_known = models.CharField(
        verbose_name=('Is patient aware that cancer is suspected '
                      'as a diagnosis?'),
        choices=YES_NO,
        max_length=3)

    enrollment_clinic_visit_method = models.CharField(
        verbose_name=('How did patient get to enrollment clinic visit?'),
        max_length=50)

    slh_travel = models.CharField(
        verbose_name=('If you had to travel to SLH to see a doctor, how '
                      'would you go about it?'),
        max_length=50)

    tests_ordered = models.CharField(
        verbose_name=('Does patient report any tests being ordered or '
                      'done at or since enrollment visit?'),
        choices=YES_NO,
        max_length=3)

    tests_type = models.CharField(
        verbose_name=('If yes, type of test'),
        choices=TEST_TYPE,
        max_length=15,
        blank=True,
        null=True)

    tests_type_other = OtherCharField(
        max_length=15,
        blank=True,
        null=True)

    biospy_part = models.CharField(
        verbose_name=('Describe part of body where biopsy was performed'),
        max_length=15,
        blank=True,
        null=True)

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
        choices=PATIENT_FACTOR,
        max_length=50,
        null=True,
        blank=True)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Patient call - Initial'
        verbose_name_plural = 'Patient call - Initial'
