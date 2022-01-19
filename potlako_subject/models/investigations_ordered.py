from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from ..choices import DATE_ESTIMATION
from ..choices import FACILITY, LAB_TESTS, LAB_TESTS_STATUS
from .list_models import ImagingTestType, PathologyTest, TestsOrderedType
from .model_mixins import CrfModelMixin


class LabTestManager(models.Manager):

    def get_by_natural_key(self, lab_test_type, lab_test_date, investigations):
        return self.get(lab_test_type=lab_test_type,
                        lab_test_date=lab_test_date,
                        investigations=investigations)


class InvestigationsOrdered(CrfModelMixin):

    tests_ordered_type = models.ManyToManyField(
        TestsOrderedType,
        verbose_name='What tests were ordered?')

    tests_ordered_type_other = OtherCharField()

    facility_ordered = models.CharField(
        verbose_name='Add facility where labs/tests were ordered"',
        max_length=40,
        choices=FACILITY,
        blank=True,
        null=True,)

    facility_ordered_other = OtherCharField()

    ordered_date = models.DateField(
        verbose_name='Date of clinic visit when labs/tests were ordered"',
        validators=[date_not_before_study_start],
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
        verbose_name='If biopsy, specify site',
        max_length=25,
        blank=True,
        null=True)

    fna_location = OtherCharField(
        verbose_name='If FNA, please indicate location',
        max_length=25,
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

    specimen_tracking_notes = models.TextField(
        verbose_name=('Path specimen tracking notes'),
        max_length=1500,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Investigations - Ordered'
        verbose_name_plural = 'Investigations - Ordered'


class LabTest(SiteModelMixin, BaseUuidModel):

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
        verbose_name='Lab test status.',
        choices=LAB_TESTS_STATUS,
        max_length=50)

    lab_test_status_other = OtherCharField(
        verbose_name='If other lab test results status, specify details',
        max_length=50,
        blank=True,
        null=True)

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = LabTestManager()

    def natural_key(self):
        return (self.lab_test_type, self.lab_test_date) + self.investigations.natural_key()

    natural_key.dependencies = ['sites.Site']

    class Meta:
        unique_together = ('investigations', 'lab_test_type', 'lab_test_date')
