from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django_crypto_fields.fields import (
    IdentityField, FirstnameField, LastnameField)
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, date_not_future
from edc_base.model_validators import date_is_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import age, get_utcnow
from edc_constants.choices import YES_NO, GENDER, POS_NEG_UNKNOWN

from ..choices import CLINICIAN_TYPE, FACILITY, FACILITY_UNIT, DISPOSITION
from ..choices import KIN_RELATIONSHIP, SCALE, SEVERITY_LEVEL, NOTES
from ..choices import SUSPECTED_CANCER, TRIAGE_STATUS, DATE_ESTIMATION
from ..screening_identifier import ScreeningIdentifier
from .list_models import Symptoms


class ClinicianCallEnrollment(SiteModelMixin, BaseUuidModel):

    identifier_cls = ScreeningIdentifier

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=timezone.now,
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

    info_from_clinician = models.CharField(
        verbose_name='Did the team learn of the cancer suspect through a call '
                     'with the clinician ? ',
        max_length=3,
        choices=YES_NO,)

    info_source_specify = models.CharField(
        verbose_name='Specify how the team learnt of the cancer suspect',
        max_length=50,
        blank=True,
        null=True)

    call_clinician_type = models.CharField(
        verbose_name='Type of clinician spoken to on the phone',
        choices=CLINICIAN_TYPE,
        max_length=50,)

    received_training = models.CharField(
        verbose_name='Has the clinician received Potlako+ training',
        choices=YES_NO,
        max_length=3,)

    call_clinician_other = models.CharField(
        max_length=50,
        verbose_name='If \'Other type\', specify the type of clinician',
        blank=True,
        null=True)

    consented_contact = models.CharField(
        verbose_name='Did the potential participant, consent to being '
                     'contacted by Potlako+ team',
        max_length=3,
        choices=YES_NO)

    paper_register = models.CharField(
        verbose_name='Has patient been entered in Potlako+ paper register?',
        choices=YES_NO,
        max_length=3,)

    facility = models.CharField(
        verbose_name='Name of facility visited at enrollment',
        choices=FACILITY,
        max_length=30)

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
        unique=True)

    hospital_identity = IdentityField(
        verbose_name='Patient hospital ID number (if available)',
        blank=True,
        null=True)

    last_name = LastnameField(
        verbose_name='Patient surname',
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

    kgotla = models.CharField(
        verbose_name='Kgotla where patient resides',
        max_length=50)

    nearest_facility = models.CharField(
        verbose_name='Nearest primary clinic or health post to where'
                     ' patient resides',
        choices=FACILITY,
        max_length=30,)

    nearest_facility_other = OtherCharField()

    primary_cell = EncryptedCharField(
        verbose_name='Patient phone number 1 (Primary)',
        max_length=8,
        validators=[CellNumber, ],
        blank=False,
        null=False)

    secondary_cell = EncryptedCharField(
        verbose_name='Patient phone number 2 (Secondary)',
        max_length=8,
        validators=[CellNumber, ])

    kin_lastname = LastnameField(
        verbose_name='Next of kin 1 Surname',
        blank=False,
        null=False)

    kin_firstname = FirstnameField(
        verbose_name='Next of kin 1 First name',
        blank=False,
        null=False)

    kin_relationship = models.CharField(
        verbose_name='Next of kin 1 relationship',
        choices=KIN_RELATIONSHIP,
        max_length=20,)

    kin_relation_other = OtherCharField(
        verbose_name='If other, describe next of kin 1 relationship',
        max_length=50,
        blank=True,
        null=True,
    )

    kin_cell = EncryptedCharField(
        verbose_name='Next of kin 1 phone number',
        validators=[CellNumber, ],
        blank=False,
        null=False)

    other_kin_avail = models.CharField(
        verbose_name='Next of kin 2 details available?',
        choices=YES_NO,
        max_length=3)

    other_kin_lastname = LastnameField(
        verbose_name='Next of kin 2 Surname',)

    other_kin_firstname = FirstnameField(
        verbose_name='Next of kin 2 First name',)

    other_kin_rel = models.CharField(
        verbose_name='Next of kin 2 relationship',
        choices=KIN_RELATIONSHIP,
        max_length=20,
        blank=True,
        null=True,)

    other_kin_rel_other = OtherCharField(
        verbose_name='If other, describe next of kin 2 relationship',
        max_length=50,
        blank=True,
        null=True,)

    other_kin_cell = EncryptedCharField(
        verbose_name='Next of kin 2 phone number',
        validators=[CellNumber, ])

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
        verbose_name='Date of earliest onset symptom(s)')

    early_symptoms_date_estimated = models.CharField(
        verbose_name='Is the symptoms date estimated?',
        choices=YES_NO,
        max_length=3)

    early_symptoms_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=6,
        blank=True,
        null=True,
    )

    symptoms_details = models.TextField(
        verbose_name='Details of symptom duration',
        max_length=100,)

    suspected_cancer = models.CharField(
        verbose_name='Suspected Cancer type',
        max_length=30,
        choices=SUSPECTED_CANCER,
        help_text='((if clinician unsure, select \'unsure\'))',)

    suspected_cancer_other = OtherCharField(
        verbose_name='If other suspected Cancer type, please specify',
        max_length=30,)

    suspicion_level = models.CharField(
        verbose_name='How strong is clinician\'s suspicion for cancer?',
        choices=SEVERITY_LEVEL,
        max_length=10,)

    performance = models.IntegerField(
        verbose_name='Performance Status (ECOG)',
        default=1,
        choices=SCALE,
        validators=[MaxValueValidator(5), MinValueValidator(1)],)

    pain_score = models.IntegerField(
        default=1,
        choices=SCALE,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text='(confirm with clinician that this is out of total '
                  'score of 5)',)

    last_hiv_result = models.CharField(
        verbose_name='What was the patient\'s last HIV result?',
        choices=POS_NEG_UNKNOWN,
        max_length=10,)

    patient_disposition = models.CharField(
        verbose_name='What was the patient\'s disposition at the end of '
                     'this visit?',
        max_length=6,
        choices=DISPOSITION,)

    referral_reason = models.TextField(
        verbose_name='Reason for referral',
        max_length=100,
        blank=True,
        null=True,)

    referral_date = models.DateField(
        verbose_name='Next appointment date',
        default=timezone.now,
        validators=[date_is_future, ],
        blank=True,
        null=True,)

    referral_facility = models.CharField(
        verbose_name='Name and type of facility patient being referred to'
                     '(referral facility)',
        max_length=30,
        choices=FACILITY,
        blank=True,
        null=True,)

    referral_facility_other = OtherCharField()

    referral_unit = models.CharField(
        verbose_name='Unit where patient is being referred to',
        choices=FACILITY_UNIT,
        max_length=20,
        blank=True,
        null=True,)

    referral_discussed = models.CharField(
        verbose_name='Was referral discussed with receiving clinician?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    clinician_designation = models.CharField(
        verbose_name='Designation of referral clinician patient discussed with',
        help_text='(If designation is not specified or unknown, plese write "UNK")',
        max_length=50,
        blank=True,
        null=True,)

    referral_fu_date = models.DateField(
        verbose_name='Date of appointment for return visit to referring '
                     'facility',
        blank=True,
        null=True,)

    triage_status = models.CharField(
        verbose_name='What is patient\'s triage status?',
        choices=TRIAGE_STATUS,
        max_length=10,)

    investigated = models.CharField(
        verbose_name='Were there any investigations ordered or performed '
                     'during this visit?',
        choices=YES_NO,
        max_length=3,)

    notes = models.TextField(
        verbose_name='Notes on investigations ordered - continue to Labs '
                     'only after tests have been done',
        max_length=25,
        choices=NOTES,
        blank=True,
        null=True,
        help_text='(COMPLETE \'INVESTIGATIONS FORM\' AFTER TESTS HAVE BEEN '
                  'COMPLETED)')

    comments = models.TextField(
        verbose_name=('Are there any other comments regarding this '
                      'enrollment vist?'),
        max_length=150,
        blank=True,
        null=True,)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Clinician call - Enrollment'
        verbose_name_plural = 'Clinician call - Enrollment'

    def save(self, *args, **kwargs):
        age_delta = age(self.dob, get_utcnow())
        self.age_in_years = age_delta.years
        if not self.id:
            self.screening_identifier = self.identifier_cls().identifier
            self.contact_date = self.report_datetime
        super(ClinicianCallEnrollment, self).save(*args, **kwargs)
