from django.db import models
from edc_base.model_validators import datetime_not_future, date_is_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_mixins import BaseUuidModel

from ..choices import ALIVE_DEAD_LTFU, CLINICIAN_TYPE, FACILITY, VISIT_TYPE
from .model_mixins import ModelCsvFormExportMixin


class HomeVisit(BaseUuidModel):

    model_csv_form_export = ModelCsvFormExportMixin

    visit_date_time = models.DateTimeField(
        verbose_name='Date of Visit',
        validators=[datetime_not_before_study_start, datetime_not_future])

    clinician_name = models.CharField(
        verbose_name='Name of clinician1 who made the home visit',
        max_length=25,)

    clinician_type = models.CharField(
        verbose_name='Type of clinician1 who made the home visit',
        choices=CLINICIAN_TYPE,
        max_length=50)

    facility_clinician_works = models.CharField(
        verbose_name='Name of facility where clinician1 works',
        choices=FACILITY,
        max_length=30)

    clinician_two_name = models.CharField(
        verbose_name='Name of clinician2 who made the home visit',
        max_length=25,)

    clinician_two_type = models.CharField(
        verbose_name='Type of clinician2 who made the home visit',
        choices=CLINICIAN_TYPE,
        max_length=50)

    clinician_two_facility = models.CharField(
        verbose_name='Name of facility where clinician2 works',
        choices=FACILITY,
        max_length=30)

    clinician_three_name = models.CharField(
        verbose_name='Name of clinician3 who made the home visit',
        max_length=25,)

    clinician_three_type = models.CharField(
        verbose_name='Type of clinician3 who made the home visit',
        choices=CLINICIAN_TYPE,
        max_length=50)

    clinician_three_facility = models.CharField(
        verbose_name='Name of facility where clinician3 works',
        choices=FACILITY,
        max_length=30)

    visit_outcome = models.CharField(
        verbose_name='Outcome of home visit',
        choices=ALIVE_DEAD_LTFU,
        max_length=30,
        help_text='(IF DIED OR LTFU, COMPLETE \'EXIT FORM\')')

    next_appointment = models.DateField(
        verbose_name='If alive, next appointment date',
        validators=[date_is_future, ],
        blank=True,
        null=True,)

    next_ap_facility = models.CharField(
        verbose_name='If alive, next appointment facility',
        choices=FACILITY,
        max_length=30,
        blank=True,
        null=True,)

    nex_ap_type = models.CharField(
        verbose_name='If alive, next appointment type',
        choices=VISIT_TYPE,
        max_length=8,
        blank=True,
        null=True,)

    general_comments = models.TextField(
        verbose_name='General comments on home visit (including if patient '
                     'alive reasons for missing appointments)',
        max_length=150,
        blank=True,
        null=True)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Home Visit'
