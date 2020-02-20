from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future, date_is_future
from edc_base.utils import get_utcnow
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO

from ..choices import (FACILITY, VISIT_TYPE, DETERMINE_MISSED_VISIT,
                       PEOPLE_INQUIRED_FROM, REASON_MISSED_VISIT)
from .model_mixins import ModelCsvFormExportMixin


class MissedVisit(BaseUuidModel):

    model_csv_form_export = ModelCsvFormExportMixin

    report_datetime = models.DateTimeField(
        verbose_name='Datetime \'missed visit\' form entered',
        default=get_utcnow,
    )

    missed_visit_date = models.DateField(
        verbose_name='Date of reference missed visit (visit previously '
                     'scheduled that patient missed)',
        default=get_utcnow,
        validators=[date_not_future, ],)

    facility_scheduled = models.CharField(
        verbose_name='Facility where missed appointment was scheduled',
        choices=FACILITY,
        max_length=30,)

    visit_type = models.CharField(
        verbose_name='Type of visit missed',
        choices=VISIT_TYPE,
        max_length=10,)

    determine_missed = models.CharField(
        verbose_name='How was missed visit determined?',
        choices=DETERMINE_MISSED_VISIT,
        max_length=100,)

    inquired = models.CharField(
        verbose_name='Was patient or next of kin called to inquire '
                     'about the missed call',
        choices=YES_NO,
        max_length=3,)

    inquired_from = models.CharField(
        verbose_name='Who was the phone call to?',
        choices=PEOPLE_INQUIRED_FROM,
        max_length=100,)

    reason_missed = models.CharField(
        verbose_name='Reason for missed visit',
        choices=REASON_MISSED_VISIT,
        max_length=50,)

    reason_other = OtherCharField(
        verbose_name='If other, describe reason for missed visit',
        max_length=50,
        blank=True,
        null=True,)

    next_appointment = models.DateField(
        verbose_name='Date of next appointment',
        default=get_utcnow,
        validators=[date_is_future, ],)

    next_ap_facility = models.CharField(
        verbose_name='Facility at next appointment',
        choices=FACILITY,
        max_length=30,)

    next_ap_type = models.CharField(
        verbose_name='Type of next appointment',
        choices=VISIT_TYPE,
        max_length=10,)

    home_visit = models.CharField(
        verbose_name='Should home visit be arranged?',
        choices=YES_NO,
        max_length=3,
        help_text='(After 3 patient and 3 next of kin phone attempts '
                  'made)',)

    transport_need = models.CharField(
        verbose_name='Has patient expressed need for transportation '
                     'or is he/she already receiving transport support?',
        choices=YES_NO,
        max_length=3,)

    clinician_name = models.CharField(
        verbose_name='Name of clinician (and indicate whether doctor or '
                     'nurse) that coordinator discussed missed visit with',
        max_length=50,)

    comments = models.TextField(
        verbose_name='Any other general comments about missed visit '
                     'encounter?',
        max_length=150,
        help_text='(Note that this form may involve multiple phone'
                  'calls (e.g. with clinician, patient and then'
                  'clinician again))',
        blank=True,
        null=True,)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Missed Visit'
