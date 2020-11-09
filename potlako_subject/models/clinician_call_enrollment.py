from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django_crypto_fields.fields import (
    IdentityField, FirstnameField, LastnameField)
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, date_not_future, datetime_not_future
from edc_base.model_validators import TelephoneNumber
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO, GENDER, POS_NEG_UNKNOWN, YES_NO_NA
from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import NOT_APPLICABLE

from ..choices import CANCER_SUSPECT, ENROLLMENT_SITES
from ..choices import CLINICIAN_TYPE, FACILITY, FACILITY_UNIT, DISPOSITION
from ..choices import KIN_RELATIONSHIP, SCALE, SEVERITY_LEVEL, PAIN_SCORE
from ..choices import SUSPECTED_CANCER, TRIAGE_STATUS, DATE_ESTIMATION
from ..eligibility import Eligibility
from ..screening_identifier import ScreeningIdentifier
from .list_models import Symptoms
from .validators import datetime_not_now, identity_check
from edc_base.utils import get_utcnow


class ClinicianCallEnrollmentManager(models.Manager):
    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)
    
class ClinicianCallEnrollment(SiteModelMixin, BaseUuidModel):

    identifier_cls = ScreeningIdentifier
    eligibility_cls = Eligibility

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ],
        help_text='Date and time of report.')

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        unique=True,
        editable=False)

    reg_date = models.DateField(
        verbose_name='Date of visit when patient was registered '
                     'at facility',
        default=timezone.now,
        validators=[date_not_future, ],)

    contact_date = models.DateField(
        verbose_name='Date Potlako+ staff member learnt of the cancer suspect')

    cancer_suspect = models.CharField(
        verbose_name='How did the team learn of the cancer suspect?',
        max_length=31,
        choices=CANCER_SUSPECT,)

    cancer_suspect_other = OtherCharField()

    received_training = models.CharField(
        verbose_name='Has the clinician received Potlako+ training',
        choices=YES_NO,
        max_length=3,)

    call_clinician_type = models.CharField(
        verbose_name='Type of clinician spoken to on the phone',
        choices=CLINICIAN_TYPE,
        max_length=50,
        blank=True,
        null=True,)

    call_clinician_other = models.CharField(
        max_length=50,
        verbose_name='If \'Other type\', specify the type of clinician',
        blank=True,
        null=True)

    consented_contact = models.CharField(
        verbose_name='Did the potential participant, agree to being '
                     'contacted by Potlako+ team',
        max_length=3,
        choices=YES_NO)

    paper_register = models.CharField(
        verbose_name='Has patient been entered in Potlako+ paper register?',
        choices=YES_NO,
        max_length=3,)

    facility = models.CharField(
        verbose_name='Name of facility visited at enrollment',
        choices=ENROLLMENT_SITES,
        max_length=40)

    facility_other = OtherCharField()

    facility_unit = models.CharField(
        verbose_name='Unit at facility where patient was seen at '
                     'enrollment',
        choices=FACILITY_UNIT,
        max_length=20,)

    unit_other = models.TextField(
        max_length=250,
        verbose_name='If \'Other\', describe unit at facility '
                     'where patient was seen at enrollment',
        blank=True,
        null=True)

    """ Patient's Personal Details & Identity """
    national_identity = IdentityField(
        verbose_name='Patient ID number (Omang)',
        validators=[identity_check, ],
        unique=True)

    hospital_identity = IdentityField(
        verbose_name='Patient hospital ID number (if available)',
        blank=True,
        null=True)

    last_name = LastnameField(
        verbose_name='Patient last name',
        blank=False,)

    first_name = FirstnameField(
        verbose_name='Patient first name',
        blank=False,)

    other_names = models.CharField(
        verbose_name='Patient other names',
        max_length=50,
        blank=True,
        null=True,)

    age_in_years = models.IntegerField(
        verbose_name='How old is the patient?',
        help_text='(Years)',
        blank=False)

    gender = models.CharField(
        verbose_name='Gender',
        choices=GENDER,
        max_length=1,)

    village_town = models.CharField(
        verbose_name='Village or Town where patient resides',
        max_length=50)

    patient_contact = models.CharField(
        verbose_name=('Does patient have a cell phone number or telephone '
                      'number?'),
        choices=YES_NO,
        max_length=3,)

    primary_cell = EncryptedCharField(
        verbose_name='Patient phone number 1 (Primary)',
        max_length=8,
        validators=[CellNumber, ])

    secondary_cell = EncryptedCharField(
        verbose_name='Patient phone number 2 (Secondary)',
        max_length=8,
        validators=[CellNumber, ])

    telephone_number = EncryptedCharField(
        verbose_name='Patient telephone number',
        max_length=7,
        validators=[TelephoneNumber, ])

    kin_details_provided = models.CharField(
        verbose_name='Did the patient give details of next of kin?',
        max_length=3,
        choices=YES_NO)

    clinician_type = models.CharField(
        verbose_name='Type of clinician (or most senior clinician) '
                     'who saw the patient',
        choices=CLINICIAN_TYPE,
        max_length=50,)

    clinician_other = OtherCharField(
        verbose_name='If Other type, describe type of clinician (or the'
                     ' most senior clinician) who saw patient',
        max_length=50,)

    symptoms = models.ManyToManyField(
        Symptoms,
        verbose_name='Presenting symptom(s)',
        help_text='(select all that apply)')

    symptoms_other = OtherCharField()

    early_symptoms_date = models.DateField(
        verbose_name='Date of earliest onset symptom(s)',
        validators=[date_not_future, datetime_not_now])

    early_symptoms_date_estimated = models.CharField(
        verbose_name='Is the symptoms date estimated?',
        choices=YES_NO,
        max_length=3)

    early_symptoms_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True
    )

    suspected_cancer = models.CharField(
        verbose_name='Suspected Cancer type',
        max_length=30,
        choices=SUSPECTED_CANCER,
        help_text='(if clinician unsure, select \'unsure\')',)

    suspected_cancer_unsure = models.TextField(
        verbose_name=('If unsure of cancer type, kindly list all suspected '
                      'cancer types'),
        max_length=60,
        blank=True,
        null=True)

    suspected_cancer_other = OtherCharField(
        verbose_name='If other suspected Cancer type, please specify',
        max_length=30,)

    suspicion_level = models.CharField(
        verbose_name='How strong is clinician\'s suspicion for cancer?',
        choices=SEVERITY_LEVEL,
        max_length=10,)

    performance = models.IntegerField(
        verbose_name='Performance Status (ECOG)',
        default=0,
        choices=SCALE,
        validators=[MaxValueValidator(5), MinValueValidator(0)],)

    pain_score = models.CharField(
        default='0_no_pain',
        choices=PAIN_SCORE,
        max_length=15)

    last_hiv_result = models.CharField(
        verbose_name='What was the patient\'s last HIV result?',
        choices=POS_NEG_UNKNOWN,
        max_length=10,)

    patient_disposition = models.CharField(
        verbose_name='What was the patient\'s disposition at the end of '
                     'this visit?',
        max_length=10,
        choices=DISPOSITION,)

    referral_reason = models.TextField(
        verbose_name='Reason for referral',
        max_length=100,
        blank=True,
        null=True,)

    referral_date = models.DateField(
        verbose_name='Next appointment date',
        blank=True,
        null=True,)

    referral_facility = models.CharField(
        verbose_name='Name and type of facility patient being referred to'
                     '(referral facility)',
        max_length=40,
        choices=FACILITY,
        blank=True,
        null=True,)

    referral_facility_other = OtherCharField()

    referral_unit = models.CharField(
        verbose_name='Unit where patient is being referred to',
        choices=FACILITY_UNIT,
        max_length=20,
        default=NOT_APPLICABLE)

    referral_unit_other = OtherCharField()

    referral_discussed = models.CharField(
        verbose_name='Was referral discussed with receiving clinician?',
        choices=YES_NO_NA,
        max_length=3,
        default=NOT_APPLICABLE)

    triage_status = models.CharField(
        verbose_name='What is patient\'s triage status?',
        choices=TRIAGE_STATUS,
        max_length=10,)

    investigated = models.CharField(
        verbose_name='Were there any investigations ordered or performed '
                     'during this visit?',
        choices=YES_NO_UNKNOWN,
        max_length=7,)

    tests_ordered = models.TextField(
        verbose_name='Indicate which tests were ordered.',
        max_length=255,
        blank=True, null=True, )

    comments = models.TextField(
        verbose_name=('Are there any other comments regarding this '
                      'enrollment visit?'),
        max_length=150,
        blank=True,
        null=True,)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)
    
    objects = ClinicianCallEnrollmentManager()
    
    def natural_key(self):
        return(self.screening_identifier)
    natural_key.dependencies = ['sites.Site']

    def save(self, *args, **kwargs):
        if not self.id:
            self.screening_identifier = self.identifier_cls().identifier
            self.contact_date = self.report_datetime

        eligibility_obj = self.eligibility_cls(
            age_in_years=self.age_in_years,
            consented_contact=self.consented_contact)
        self.is_eligible = eligibility_obj.is_eligible
        if eligibility_obj.reasons_ineligible:
            self.ineligibility = eligibility_obj.reasons_ineligible
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Clinician call - Enrollment'
        verbose_name_plural = 'Clinician call - Enrollment'



class NextOfKinManager(models.Manager):
    def get_by_natural_key(self, kin_cell, kin_telephone, clinician_call_enrollemt):
        return self.get(clinician_call_enrollemt=clinician_call_enrollemt,
                        kin_cell=kin_cell,
                        kin_telephone=kin_telephone)
    
    
class NextOfKin(BaseUuidModel):

    clinician_call_enrollemt = models.ForeignKey(ClinicianCallEnrollment,
                                                 on_delete=PROTECT)

    kin_lastname = LastnameField(
        verbose_name='Next of kin Surname',
        blank=False,
        null=False)

    kin_firstname = FirstnameField(
        verbose_name='Next of kin First name',
        blank=False,
        null=False)

    kin_relationship = models.CharField(
        verbose_name='Next of kin relationship',
        choices=KIN_RELATIONSHIP,
        max_length=20,
        blank=False,
        null=False)

    kin_relation_other = OtherCharField(
        verbose_name='If other, describe next of kin relationship',
        max_length=50,
        blank=True,
        null=True,
    )

    kin_cell = EncryptedCharField(
        verbose_name='Next of kin cellphone number',
        validators=[CellNumber, ],
        blank=True,
        null=True)

    kin_telephone = EncryptedCharField(
        verbose_name='Next of kin telephone number',
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)
    
    history = HistoricalRecords()
    
    objects = NextOfKinManager()
    
    def natural_key(self):
        return (self.kin_cell, self.kin_telephone,) + self.clinician_call_enrollemt.natural_key()
    natural_key.dependencies = ['potlako_plus.cliniciancallenrollment']
    
    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Next Of Kin'
        unique_together = ('clinician_call_enrollemt', 'kin_cell', 'kin_telephone')
