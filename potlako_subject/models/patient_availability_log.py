from datetime import date
from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_search.model_mixins import SearchSlugManager

from ..choices import CANT_TALK_REASON
from .clinician_call_enrollment import ClinicianCallEnrollment


class PatientAvailabilityLogManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(
            clinician_call__screening_identifier=screening_identifier,
        )


class PatientAvailabilityLogEntryManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier, report_datetime):
        return self.get(
            patient_availability_log__clinician_call__screening_identifier=screening_identifier,
            report_datetime=report_datetime
        )


class PatientAvailabilityLog(BaseUuidModel):

    clinician_call = models.OneToOneField(
        ClinicianCallEnrollment,
        on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name='Report date',
        default=get_utcnow)

    history = HistoricalRecords()

    objects = PatientAvailabilityLogManager()

    def __str__(self):
        return self.clinician_call.screening_identifier

    def natural_key(self):
        return (self.clinician_call.screening_identifier,)


class PatientAvailabilityLogEntry(BaseUuidModel):

    patient_availability_log = models.ForeignKey(
        PatientAvailabilityLog,
        on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[datetime_not_future],
        default=get_utcnow)

    can_take_call = models.CharField(
        verbose_name='Does the participant have time to take a call?',
        choices=YES_NO,
        max_length=6)

    reason = models.CharField(
        verbose_name='Reason',
        choices=CANT_TALK_REASON,
        max_length=100,
        blank=True,
        null=True)

    reason_other = OtherCharField()

    comment = EncryptedTextField(
        verbose_name="Comments",
        max_length=250,
        null=True,
        blank=True,)

    date_created = models.DateField(
        default=date.today)

    objects = PatientAvailabilityLogEntryManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.patient_availability_log.clinician_call.screening_identifier} ' \
               f'({self.report_datetime})'

    def natural_key(self):
        return (self.report_datetime,) + self.patient_availability_log.natural_key()

    class Meta:
        app_label = 'potlako_subject'
        unique_together = ('patient_availability_log', 'report_datetime')
        ordering = ('report_datetime',)
