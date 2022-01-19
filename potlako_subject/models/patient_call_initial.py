from datetime import timedelta

from django import forms
from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_base.utils import age, get_utcnow
from edc_constants.choices import POS_NEG_UNKNOWN, YES_NO_NA
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_protocol.validators import date_not_before_study_start

from ..choices import DATE_ESTIMATION, ENROLLMENT_VISIT_METHOD, FACILITY
from ..choices import FACILITY_UNIT, TESTS_ORDERED, DISTRICT
from ..choices import PAIN_SCORE, SCALE, EDUCATION_LEVEL, WORK_TYPE
from ..choices import UNEMPLOYED_REASON, VL_UNITS
from .list_models import PatientResidence, SmsPlatform, SourceOfInfo
from .model_mixins import CrfModelMixin


class PreviousFacilityVisitManager(models.Manager):

    def get_by_natural_key(self, facility_visited,
                           previous_facility_period, patient_call_initial):
        return self.get(facility_visited=facility_visited,
                        previous_facility_period=previous_facility_period,
                        patient_call_initial=patient_call_initial)


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
        verbose_name='where does the patient currently live?',
        choices=DISTRICT,
        max_length=50,
        blank=False,
        null=True)

    residential_district_other = OtherCharField()

    patient_kgotla = models.CharField(
        verbose_name='What is the name of the ward where the patient resides?',
        max_length=30)

    primary_clinic = models.CharField(
        verbose_name=('Nearest primary clinic or health post '
                      'to where patient resides'),
        choices=FACILITY,
        max_length=40)

    primary_clinic_other = OtherCharField()

    education_level = models.CharField(
        verbose_name='What is your highest level of education',
        max_length=15,
        choices=EDUCATION_LEVEL,
        blank=True)

    heard_of_potlako = models.CharField(
        verbose_name='Has the patient heard about Potlako+ ?',
        max_length=3,
        choices=YES_NO)

    source_of_info = models.ManyToManyField(
        SourceOfInfo,
        verbose_name='Where or who did you hear about Potlako+ from ?',
        blank=True)

    source_of_info_other = OtherCharField()

    potlako_sms_received = models.CharField(
        verbose_name='Have you received Potlako+ messages?',
        choices=YES_NO,
        max_length=3)

    sms_platform = models.ManyToManyField(
        SmsPlatform,
        verbose_name=('If yes, which Potlako+ messaging platform did you'
                      ' receive?'),
        max_length=35,
        blank=True,)

    sms_platform_other = OtherCharField()

    work_status = models.CharField(
        verbose_name='Is the patient currently working?',
        choices=YES_NO,
        max_length=3)

    work_type = models.CharField(
        verbose_name='What kind of work does the patient do?',
        choices=WORK_TYPE,
        max_length=30,
        blank=True,
        null=True)

    work_type_other = OtherCharField()

    unemployed_reason = models.CharField(
        verbose_name='Why is the patient not working?',
        choices=UNEMPLOYED_REASON,
        max_length=30,
        blank=True,
        null=True)

    unemployed_reason_other = OtherCharField()

    social_welfare = models.CharField(
        verbose_name='Is the patient on social welfare support?',
        choices=YES_NO_NA,
        max_length=30,
        default=NOT_APPLICABLE)

    medical_conditions = models.CharField(
        verbose_name='Does the patient have any other medical conditions?',
        choices=YES_NO,
        max_length=3)

    patient_residence = models.ManyToManyField(
        PatientResidence,
        verbose_name='Who does the patient stay with?',
        max_length=30,
        blank=True,)

    patient_residence_other = OtherCharField()

    other_facility = models.CharField(
        verbose_name=('Before enrollment visit, has the patient been '
                      'seen for similar symptoms at other facilities?'),
        choices=YES_NO,
        max_length=3)

    facility_number = models.IntegerField(
        verbose_name='How many facilities?',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True,
    )

    perfomance_status = models.IntegerField(
        verbose_name='Patient performance status',
        choices=SCALE,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    pain_score = models.CharField(
        verbose_name='Patient pain score',
        default='0_no_pain',
        max_length=15,
        choices=PAIN_SCORE)

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
        max_length=3,
        blank=True,
        null=True)

    hiv_test_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,
    )

    cd4_count_known = models.CharField(
        verbose_name='Do you know your recent CD4 results ?',
        choices=YES_NO,
        max_length=3)

    cd4_count = models.IntegerField(
        verbose_name='What is your recent CD4 count results?',
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
        blank=True,
        null=True,
        help_text='unit in cells/uL')

    cd4_count_date = models.DateField(
        verbose_name=('When was patient\'s recent CD4 count results?'),
        validators=[date_not_future, ],
        blank=True,
        null=True)

    cd4_count_date_estimated = models.CharField(
        verbose_name='Is the CD4 count results date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    cd4_count_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,
    )

    reason_cd4_unknown = models.TextField(
        verbose_name='Reason cd4 count results unknown',
        max_length=1000,
        blank=True,
        null=True)

    vl_results_known = models.CharField(
        verbose_name='Do you know your recent viral load results ?',
        choices=YES_NO,
        max_length=3)

    vl_results = models.CharField(
        verbose_name='What is your recent VL results?',
        choices=VL_UNITS,
        max_length=12,
        blank=True,
        null=True,)

    vl_results_date = models.DateField(
        verbose_name=('When was patient\'s recent VL results?'),
        validators=[date_not_future, ],
        blank=True,
        null=True)

    vl_results_date_estimated = models.CharField(
        verbose_name='Is the VL results date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    vl_results_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True,
    )

    reason_vl_unknown = models.TextField(
        verbose_name='Reason VL results unknown',
        max_length=1000,
        blank=True,
        null=True)

    cancer_suspicion_known = models.CharField(
        verbose_name=('Is patient aware that cancer is suspected '
                      'as a diagnosis?'),
        choices=YES_NO,
        max_length=3)

    enrollment_visit_method = models.CharField(
        verbose_name=('How did patient get to enrollment clinic visit?'),
        choices=ENROLLMENT_VISIT_METHOD,
        max_length=30)

    enrollment_visit_method_other = OtherCharField()

    slh_travel = models.CharField(
        verbose_name=('If you had to travel to (referral facility) to see a '
                      'doctor, how would you go about it?'),
        max_length=50,
        help_text='Use referral clinic name')

    tests_ordered = models.CharField(
        verbose_name=('Does patient report any tests being ordered or '
                      'done at or since enrollment visit?'),
        choices=TESTS_ORDERED,
        max_length=20)

    next_appointment_date = models.DateField(
        verbose_name='Next appointment date (per patient report)',
        blank=True,
        null=True)

    next_ap_facility = models.CharField(
        verbose_name='Next appointment facility',
        choices=FACILITY,
        max_length=40,
        help_text='per patient report')

    next_ap_facility_other = OtherCharField()

    next_ap_facility_unit = models.CharField(
        choices=FACILITY_UNIT,
        max_length=20)

    next_ap_facility_unit_other = OtherCharField(
        max_length=50)

    transport_support = models.CharField(
        verbose_name=('Has patient expressed need for transport support?'),
        choices=YES_NO_NA,
        max_length=3,
        help_text='IF YES, COMPLETE TRANSPORT FORM')

    comments = models.TextField(
        verbose_name=('Any other general comments regarding patient encouter'),
        max_length=100,
        blank=True,
        null=True)

    initial_call_end_time = models.TimeField(
        verbose_name='End of patient initial call (timestamp)',
    )

    call_duration = models.DurationField(
        verbose_name='Duration of patient initial call',
    )

    def get_call_duration(self):
        call_end = timedelta(hours=self.initial_call_end_time.hour,
                             minutes=self.initial_call_end_time.minute,
                             seconds=self.initial_call_end_time.second,
                             microseconds=self.initial_call_end_time.microsecond)

        call_start = timedelta(hours=self.patient_call_time.hour,
                               minutes=self.patient_call_time.minute,
                               seconds=self.patient_call_time.second,
                               microseconds=self.patient_call_time.microsecond)

        return call_end - call_start

    def save(self, *args, **kwargs):
        self.call_duration = self.get_call_duration()
        self.update_age()
        super().save(*args, **kwargs)

    @property
    def community_arm(self):
        onschedule_cls = django_apps.get_model('potlako_subject.onschedule')

        try:
            onschedule_obj = onschedule_cls.objects.get(
                subject_identifier=self.subject_visit.appointment.subject_identifier)
        except onschedule_cls.DoesNotExist:
            return None
        else:
            return onschedule_obj.community_arm

    def update_age(self):
        subject_identifier = self.subject_visit.appointment.subject_identifier
        subject_consent_cls = django_apps.get_model('potlako_subject.subjectconsent')
        try:
            subject_consent = subject_consent_cls.objects.get(
                subject_identifier=subject_identifier)
        except subject_consent_cls.DoesNotExist:
            raise forms.ValidationError(
                'Please complete the subject consent form before '
                'proceeding.')
        else:
            self.age_in_years = age(subject_consent.dob, get_utcnow()).years

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Patient call - Initial'
        verbose_name_plural = 'Patient call - Initial'


class PreviousFacilityVisit(SiteModelMixin, BaseUuidModel):

    patient_call_initial = models.ForeignKey(PatientCallInitial, on_delete=PROTECT)

    facility_visited = models.CharField(
        choices=FACILITY,
        verbose_name=('Which facilities has the patient '
                      'been seen for similar symptoms?'),
        max_length=40,
        blank=True,
        help_text='(select all that apply)',)

    facility_visited_other = OtherCharField(
        max_length=30,
        blank=True,
        null=True)

    previous_facility_period = models.CharField(
        verbose_name=('For how long was he/she seen at facilities '
                      'before enrollment visit?'),
        max_length=15,
        blank=True,
        null=True,
        help_text='specify variable (days, weeks, months, years)')

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = PreviousFacilityVisitManager()

    def natural_key(self):
        return (self.facility_visited, self.previous_facility_period,) + self.patient_call_initial.natural_key()

    natural_key.dependencies = ['potlako_subject.patientcallinitial']

    class Meta:
        unique_together = (
            'patient_call_initial', 'facility_visited',
            'previous_facility_period')
