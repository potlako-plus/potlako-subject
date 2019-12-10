from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_is_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..choices import CASH_TRANSFER_STATUS
from ..choices import HOUSEMATE, TRANSPORT_CRITERIA, FACILITY, TRANSPORT_TYPE
from ..choices import VEHICLE_ARR_STATUS, BUS_VOUCHER_STATUS


class Transport(models.Model):

    report_datetime = models.DateTimeField(
        verbose_name='Datetime transport form entered',
        default=get_utcnow,)

    is_criteria_met = models.CharField(
        verbose_name='Does the patient meet the criteria '
                     'for transport support',
        choices=YES_NO,
        max_length=3,)

    qualification = models.CharField(
        verbose_name='What is your highest level of education?',
        max_length=100,)

    housemate = models.CharField(
        verbose_name='Who do you live with?',
        choices=HOUSEMATE,
        max_length=30,)

    car_ownership = models.CharField(
        verbose_name='Is there a car at home?',
        choices=YES_NO,
        max_length=3,)

    criteria_met = models.CharField(
        verbose_name='What criteria has been met for transportation'
        ' support?',
        choices=TRANSPORT_CRITERIA,
        max_length=100,)

    next_visit_date = models.DateField(
        verbose_name='Visit Date for which transportation is being '
                     'planned (next visit date)',
        validators=[date_is_future, ],
        default=get_utcnow,)

    visit_facility = models.CharField(
        verbose_name='Visit facility for which transport is being '
                     'planned',
        choices=FACILITY,
        max_length=100,)

    transport_type = models.CharField(
        verbose_name='Type of transport support being arranged',
        choices=TRANSPORT_TYPE,
        max_length=100,)

    facility_vehicle_status = models.CharField(
        verbose_name='Status of facility vehicle arrangement at '
                     'end of transport planning encounter',
        choices=VEHICLE_ARR_STATUS,
        max_length=100,)

    vehicle_status_other = OtherCharField(
        verbose_name='If other facility vehicle status, describe '
                     'details',
        max_length=100,
        blank=True,
        null=True,)

    vehicle_request_date = models.DateField(
        verbose_name='Date of initial request for facility vehicle',)

    facility_personnel = models.CharField(
        verbose_name='Facility transport office personnel who received '
                     'the request',
        max_length=25,)

    bus_voucher_status = models.CharField(
        verbose_name='Status of bus voucher arrangement at end '
                     'of transport planning encounter',
        choices=BUS_VOUCHER_STATUS,
        max_length=50,)

    bus_status_other = OtherCharField(
        verbose_name='If other, describe status of transport arrangement',
        max_length=50,
        blank=True,
        null=True,)

    cash_transfer_status = models.CharField(
        verbose_name='Status of cash transfer arrangement at end '
                     'of transport planning encounter',
        choices=CASH_TRANSFER_STATUS,
        max_length=50,)

    cash_status_other = OtherCharField(
        verbose_name='If transaction did not go through, specify details',
        max_length=100,
        blank=True,
        null=True,
        help_text='(Please detail issue and action steps to resolve issue)',)

    comments = models.TextField(
        verbose_name='Any other general comments regarding transport '
                     'planning',
        max_length=150,
        help_text='(IF NOTHING TO REPORT, PLEASE WRITE "NA")',)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Transport'
        verbose_name_plural = 'Transport'
