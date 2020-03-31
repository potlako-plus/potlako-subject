from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import CellNumber
from edc_base.model_validators import date_not_future
from edc_constants.choices import POS_NEG_UNKNOWN
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from ..choices import DELAYED_REASON, HEALTH_FACTOR, PATIENT_FACTOR
from ..choices import FACILITY_UNIT, SEVERITY_LEVEL, DISTRICT, FACILITY
from .list_models import CallAchievements, Facility, TestType
from .model_mixins import CrfModelMixin


class PatientCallInitial(CrfModelMixin):

    patient_call_time = models.TimeField(
        verbose_name='Start of patient initial call (timestamp)')

    patient_call_date = models.DateField(
        verbose_name='Date of initial patient call',
        validators=[date_not_before_study_start, date_not_future])

    age_in_years = models.IntegerField(
        verbose_name='Patient age',
        help_text='(Years)',)

    residential_district = models.CharField(
        verbose_name='where do you currently live?',
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
        max_length=3,
        blank=True,
        null=True)

    primary_keen_contact = EncryptedCharField(
        verbose_name='Please enter next of kin 1 phone number',
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

    secondary_keen_contact = EncryptedCharField(
        verbose_name='Please enter next of kin 2 phone number',
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

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

    facility_visited = models.ManyToManyField(
        Facility,
        verbose_name=('Which facilities has the patient '
                      'been seen for similar symptoms?'),
        max_length=30,
        help_text='(select all that apply)')

    facility_visited_other = OtherCharField(
        max_length=30,
        blank=True,
        null=True)

    previous_facility_period = models.CharField(
        verbose_name=('For how long was he/she seen at facilities '
                      'before enrollment visit?'),
        max_length=15,
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
        choices=POS_NEG_UNKNOWN,
        max_length=10)

    hiv_test_date = models.DateField(
        verbose_name=('When was patient\'s last HIV test?'),
        validators=[date_not_future, ],
        blank=True,
        null=True,
        help_text=('If positive test, date of positive test, if negative, '
                   'date of most recent negative test'))

    hiv_test_date_estimated = models.CharField(
        verbose_name='Is the HIV test date estimated?',
        choices=YES_NO,
        max_length=3)

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

    tests_type = models.ManyToManyField(
        TestType,
        verbose_name=('If yes, type of test'),
        max_length=15,
        blank=True)

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
        default=0,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True)

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
        verbose_name='Next appointment facility',
        choices=FACILITY,
        max_length=30,
        help_text='per patient report')

    next_appointment_facility_unit = models.CharField(
        choices=FACILITY_UNIT,
        max_length=20)

    next_appointment_facility_unit_other = OtherCharField(
        max_length=50,
        blank=True,
        null=True)

    patient_understanding = models.CharField(
        verbose_name=('Is patient\'s understanding of the next appointment '
                      '(date and location) the same as clinicians?'),
        choices=YES_NO,
        max_length=3,
        help_text=('If not, inform patient of the date as specified by the '
                   'clinician. If there is a discrepancy, call clinician '
                   'to verify'))

    transport_support = models.CharField(
        verbose_name=('Has patient expressed need for transport support?'),
        choices=YES_NO,
        max_length=3,
        help_text='IF YES, COMPLETE TRANSPORT FORM')

    call_achievements = models.ManyToManyField(
        CallAchievements,
        verbose_name='What has been achieved during the call')

    clinician_information = models.CharField(
        verbose_name=('Any information to be passed back to clinician?'),
        choices=YES_NO,
        max_length=3)

    comments = models.TextField(
        verbose_name=('Any other general comments regarding patient encouter'),
        max_length=100,
        blank=True,
        null=True)

    cancer_probability = models.CharField(
        verbose_name='Cancer probability (baseline)',
        choices=SEVERITY_LEVEL,
        max_length=10)

    encounter_end_time = models.TimeField(
        verbose_name='Time at END of encounter',
    )

    initial_call_end_time = models.TimeField(
        verbose_name='End of patient initial call (timestamp)',
    )

    call_duration = models.DurationField(
        verbose_name='Duration of patient initial call',
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Patient call - Initial'
        verbose_name_plural = 'Patient call - Initial'
