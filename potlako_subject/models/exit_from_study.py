from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN

from ..choices import (
    COMPONENTS_RECEIVED, DEATH_INFO_SOURCE, DISTRICT, FACILITY, FACILITY_TYPE,
    LTFU_CRITERIA, PLACE_OF_DEATH, POS_NEG_UNKNOWN_MISSING, REASON_FOR_EXIT,
    TREATMENT_INTENT)


class ExitFromStudy(models.Model):

    exit_reason = models.CharField(
        verbose_name='Reason for exit',
        choices=REASON_FOR_EXIT,
        max_length=50,)

    general_comments = models.TextField(
        verbose_name='Any general comments about patient exit?',
        max_length=150,)

    last_visit_date = models.DateField(
        verbose_name='What was the date of patient\'s last visit?',
        validators=[date_not_future, ],)

    last_visit_facility = models.CharField(
        verbose_name='What was the facility of the patient\'s last visit',
        choices=FACILITY,
        max_length=30,)

    death_date = models.DateField(
        verbose_name='Date of patient death',
        validators=[date_not_future, ],
        blank=True,
        null=True,)

    cause_of_death = models.CharField(
        max_length=20,
        blank=True,
        null=True,)

    place_of_death = models.CharField(
        choices=PLACE_OF_DEATH,
        max_length=30,
        blank=True,
        null=True,)

    facility_patient_died = models.CharField(
        verbose_name='Name of facility where patient died',
        choices=FACILITY,
        max_length=30,
        blank=True,
        null=True,)

    death_info_source = models.CharField(
        verbose_name='Source of patient death information ',
        choices=DEATH_INFO_SOURCE,
        max_length=20,
        blank=True,
        null=True,)

    info_source_other = OtherCharField(
        verbose_name='If other source of patient death communication, '
                     'describe',
        max_length=20,)

    ltfu_criteria_met = models.CharField(
        verbose_name='Criteria met for loss to follow up',
        choices=LTFU_CRITERIA,
        max_length=50,
        blank=True,
        null=True,)

    new_kgotla_res = models.CharField(
        verbose_name='If relocated, patient\'s NEW Kgotla of residence',
        max_length=25,
        blank=True,
        null=True,)

    new_village_res = models.CharField(
        verbose_name='If relocated, patient\'s NEW village of residence',
        max_length=25,
        blank=True,
        null=True,)

    new_district_res = models.CharField(
        verbose_name='If relocated, patient\'s NEW district of residence',
        choices=DISTRICT,
        max_length=25,
        blank=True,
        null=True,)

    new_facility_name = models.CharField(
        verbose_name='If relocated, patient\'s NEW facility name',
        max_length=30,
        blank=True,
        null=True,)

    new_facility_type = models.CharField(
        verbose_name='If relocated, patient\'s NEW facility type',
        choices=FACILITY_TYPE,
        max_length=30,
        blank=True,
        null=True,)

    exit_hiv_status = models.CharField(
        verbose_name='What was patient\'s HIV status at exit?',
        choices=POS_NEG_UNKNOWN_MISSING,
        max_length=10,)

    latest_hiv_test_known = models.CharField(
        verbose_name='Is the latest HIV test date known for the patient?',
        choices=YES_NO,
        max_length=3,)

    hiv_test_date = models.DateField(
        verbose_name='If yes, please enter date of HIV test',
        blank=True,
        null=True,)

    review_flag = models.CharField(
        verbose_name='Flag for physician review',
        choices=YES_NO,
        max_length=3,)

    components_rec = models.CharField(
        verbose_name='Potlako components received (or potentially received)',
        choices=COMPONENTS_RECEIVED,
        max_length=50,)

    components_rec_other = OtherCharField(
        verbose_name='Other Potlako component received:',
        max_length=50,)

    cancer_treatment_rec = models.CharField(
        verbose_name='Was any cancer specific treatment received?',
        choices=YES_NO_UNKNOWN,
        max_length=7,
        help_text='(Example: radiation, surgery (beyond biopsy), chemotherapy,'
                  ' ART for KS, esophageal stenting)',)

    treatment_intent = models.CharField(
        verbose_name='At time of exit, what was treatment intent? ',
        choices=TREATMENT_INTENT,
        max_length=10,)

    date_therapy_started = models.DateField(
        verbose_name='Date started cancer specific therapy',
        validators=[date_not_future, ],
        blank=True,
        null=True,)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Exit from study'
        verbose_name_plural = 'Exit from study'
