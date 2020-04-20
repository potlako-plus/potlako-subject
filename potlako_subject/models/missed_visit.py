from django.db import models
from django.utils import timezone

from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future, date_is_future
from edc_constants.choices import YES_NO

from ..choices import (FACILITY, VISIT_TYPE, DETERMINE_MISSED_VISIT,
                       PEOPLE_INQUIRED_FROM, REASON_MISSED_VISIT)
from .model_mixins import CrfModelMixin


class MissedVisit(CrfModelMixin):

    report_datetime = models.DateTimeField(
        verbose_name='Date and time \'missed visit\' form entered',
        default=timezone.now,
    )

    missed_visit_date = models.DateField(
        verbose_name='Date of reference missed visit (visit previously '
                     'scheduled that patient missed)',
        default=timezone.now,
        validators=[date_not_future, ],)

    facility_scheduled = models.CharField(
        verbose_name='Facility where missed appointment was scheduled',
        choices=FACILITY,
        max_length=40,)

    facility_scheduled_other = OtherCharField()

    visit_type = models.CharField(
        verbose_name='Type of visit missed',
        choices=VISIT_TYPE,
        max_length=10,)

    determine_missed = models.CharField(
        verbose_name='How did the research team know about the miissed visit?',
        choices=DETERMINE_MISSED_VISIT,
        max_length=25,)

    determine_missed_other = OtherCharField(
        max_length=50)

    inquired = models.CharField(
        verbose_name='Was patient or next of kin called to enquire '
                     'about the missed visit?',
        choices=YES_NO,
        max_length=3,)

    not_inquired_reason = models.CharField(
        verbose_name='If no above, what was the reason?',
        choices=DETERMINE_MISSED_VISIT,
        max_length=50,)

    not_inquired_reason_other = OtherCharField(
        max_length=50)

    inquired_from = models.CharField(
        verbose_name='Who was the phone call to?',
        choices=PEOPLE_INQUIRED_FROM,
        max_length=100,
        blank=True,
        null=True)

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
        default=timezone.now,
        validators=[date_is_future, ],)

    next_ap_facility = models.CharField(
        verbose_name='Facility at next appointment',
        choices=FACILITY,
        max_length=40,)

    next_ap_facility_other = OtherCharField()

    next_ap_type = models.CharField(
        verbose_name='Type of next appointment',
        choices=VISIT_TYPE,
        max_length=10,)

    home_visit = models.CharField(
        verbose_name='Should home visit be arranged?',
        choices=YES_NO,
        max_length=3,
        help_text='(After 3 patient and 3 next of kin phone attempts '
                  'made)')

    transport_need = models.CharField(
        verbose_name='Has patient expressed need for transportation?',
        choices=YES_NO,
        max_length=3)

    transport_support = models.CharField(
        verbose_name='Is the patient already receiving transport support?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    clinician_designation = models.CharField(
        verbose_name=('What is the designation of the clinician that research '
                      'staff discussed missed visit with'),
        max_length=50,
        blank=True,
        null=True,)

    comments = models.TextField(
        verbose_name='Any other general comments about missed visit '
                     'encounter?',
        max_length=150,
        help_text='(Note that this form may involve multiple phone'
                  'calls (e.g. with clinician, patient and then'
                  'clinician again))',
        blank=True,
        null=True,)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Visit'
