from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from ..choices import DATE_ESTIMATION
from ..choices import FACILITY, IMAGING_STATUS, LAB_TESTS, LAB_TESTS_STATUS
from .list_models import ImagingTestType, PathologyTest, TestsOrderedType
from .model_mixins import CrfModelMixin


class InvestigationsOrdered(CrfModelMixin):

    tests_ordered_type = models.ManyToManyField(
        TestsOrderedType,
        verbose_name='What tests were ordered?')

    tests_ordered_type_other = OtherCharField()

    facility_ordered = models.CharField(
        verbose_name='Facility where labs were ordered',
        max_length=40,
        choices=FACILITY,
        blank=True,
        null=True,)

    facility_ordered_other = OtherCharField()

    ordered_date = models.DateField(
        verbose_name='Date of clinic visit where labs were ordered',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True,)

    ordered_date_estimated = models.CharField(
        verbose_name='Is the ordered date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    ordered_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True,)

    pathology_test = models.ManyToManyField(
        PathologyTest,
        verbose_name='Type of pathology test',
        blank=True,)

    pathology_test_other = OtherCharField()

    biopsy_specify = OtherCharField(
        verbose_name='If biopsy, please describe',
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

    imaging_test_status = models.CharField(
        choices=IMAGING_STATUS,
        max_length=15,
        blank=True,
        null=True)

    imaging_test_type = models.ManyToManyField(
        ImagingTestType,
        blank=True)

    xray_tests = models.CharField(
        verbose_name='If XRay tests ordered, specify',
        max_length=25,
        blank=True,
        null=True)

    ultrasound_tests = models.CharField(
        verbose_name='If ultrasound tests ordered, specify',
        max_length=25,
        blank=True,
        null=True)

    ct_tests = models.CharField(
        verbose_name='If CT tests ordered, specify',
        max_length=25,
        blank=True,
        null=True)

    mri_tests = models.CharField(
        verbose_name='If MRI tests ordered, specify',
        max_length=25,
        blank=True,
        null=True)

    imaging_tests_type_other = OtherCharField(
        verbose_name='If other tests ordered, specify',
        max_length=25,
        blank=True,
        null=True)

    imaging_tests_date = models.DateField(
        verbose_name='Date imaging test performed (completed)',
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Investigations - Ordered'
        verbose_name_plural = 'Investigations - Ordered'


class LabTest(BaseUuidModel):

    investigations = models.ForeignKey(InvestigationsOrdered, on_delete=PROTECT)

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
