from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from ..choices import CANCER_STAGES, FACILITY, LAB_TESTS, LAB_TESTS_STATUS
from ..choices import IMAGING_STATUS, IMAGING_TESTS, PATHOLOGY_TEST_TYPE

from .model_mixins import CrfModelMixin


class Investigations(CrfModelMixin, BaseUuidModel):

    start_time = models.TimeField(
        verbose_name='Investigations: start time')

    facility_ordered = models.CharField(
        verbose_name='Facility where labs were ordered',
        max_length=25,
        choices=FACILITY)

    ordered_date = models.DateField(
        verbose_name='Date of clinic visit where labs were ordered',
        validators=[date_not_before_study_start, date_not_future])

    lab_tests_ordered = models.CharField(
        verbose_name='Were lab tests ordered??',
        choices=YES_NO,
        max_length=3)

    pathology_tests_ordered = models.CharField(
        verbose_name='Were pathology tests ordered?',
        choices=YES_NO,
        max_length=3)

    pathology_test = models.CharField(
        verbose_name='Type of pathology test',
        choices=PATHOLOGY_TEST_TYPE,
        max_length=25,
        blank=True,
        null=True)

    biopsy_other = OtherCharField(
        verbose_name='If other biopsy, please describe',
        max_length=25,
        blank=True,
        null=True)

    fna_location = OtherCharField(
        verbose_name='If FNA, please indicate location',
        max_length=25,
        blank=True,
        null=True)

    pathology_specimen_date = models.DateField(
        verbose_name='Date pathology specimen taken',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_nhl_date = models.DateField(
        verbose_name='Date pathology specimen received at NHL',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_result_date = models.DateField(
        verbose_name='Date pathology results reported',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_received_date = models.DateField(
        verbose_name='Date pathology results received by clinician',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    pathology_communicated_date = models.DateField(
        verbose_name='Date pathology results communicated to patient',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    imaging_tests = models.CharField(
        verbose_name='Were imaging tests conducted during this encounter?',
        choices=YES_NO,
        max_length=3)

    imaging_test_status = models.CharField(
        choices=IMAGING_STATUS,
        max_length=15,
        blank=True,
        null=True)

    imaging_test_type = models.CharField(
        choices=IMAGING_TESTS,
        max_length=20,
        blank=True,
        null=True)

    ultrasound_tests_other = OtherCharField(
        verbose_name='Types of ultrasound tests ordered (other, specify)',
        max_length=25,
        blank=True,
        null=True)

    imaging_tests_other = OtherCharField(
        verbose_name='Types of imaging tests ordered (other, specify)',
        max_length=25,
        blank=True,
        null=True)

    imaging_tests_date = models.DateField(
        verbose_name='Date imaging test performed (completed)',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    specimen_tracking_notes = models.TextField(
        verbose_name=('Path specimen tracking notes'),
        max_length=100,
        blank=True,
        null=True)

    diagnosis_results = models.CharField(
        verbose_name='Diagnosis results (provider)',
        choices=IMAGING_TESTS,
        max_length=20,
        blank=True,
        null=True)

    cancer_type = models.CharField(
        verbose_name='If cancer, type of cancer diagnosed',
        max_length=15,
        blank=True,
        null=True)

    diagnoses_made = models.CharField(
        verbose_name='If not cancer, diagnosis made',
        max_length=15,
        blank=True,
        null=True)

    cancer_stage = models.CharField(
        verbose_name='If cancer, stage of cancer',
        choices=CANCER_STAGES,
        max_length=10,
        blank=True,
        null=True)

    cancer_stage_other = OtherCharField(
        verbose_name='If other cancer stage, specify',
        max_length=10,
        blank=True,
        null=True)

    bpcc_enrolled = models.CharField(
        verbose_name='Participant enrolled in BPCC?',
        choices=YES_NO,
        max_length=3)

    bpcc_identifier = models.CharField(
        verbose_name='BPCC identifier (BID)',
        max_length=25)

    end_time = models.DurationField(
        verbose_name='Investigations: end time',
    )

    class Meta:
        pass


class LabTest(BaseUuidModel):

    investigations = models.ForeignKey(Investigations, on_delete=PROTECT)

    lab_test_type = models.CharField(
        verbose_name='Type of lab test.',
        choices=LAB_TESTS,
        max_length=25,
        help_text='(IF PATIENT CALL, ONLY ASK ABOUT RFT, FBC, LFT )')

    lab_test_date = models.DateField(
        verbose_name='Date of lab test.')

    lab_test_type_other = OtherCharField(
        verbose_name='If other lab test, specify',
        max_length=50,
        blank=True,
        null=True)

    lab_test_status = models.CharField(
        verbose_name='Type of lab test.',
        choices=LAB_TESTS_STATUS,
        max_length=50)

    lab_test_status_other = OtherCharField(
        verbose_name='If other lab test results status, specify details',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        pass
