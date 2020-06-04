from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_is_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..choices import CASH_TRANSFER_STATUS
from ..choices import FACILITY, TRANSPORT_TYPE
from ..choices import VEHICLE_ARR_STATUS, BUS_VOUCHER_STATUS
from .list_models import Housemate, TransportCriteria
from .model_mixins import CrfModelMixin


class Transport(CrfModelMixin):

    is_criteria_met = models.CharField(
        verbose_name='Does the patient meet the criteria '
                     'for transport support',
        choices=YES_NO,
        max_length=3,)

    housemate = models.ManyToManyField(
        Housemate,
        verbose_name='Who do you live with?')

    housemate_other = OtherCharField()

    car_ownership = models.CharField(
        verbose_name='Is there a car at home?',
        choices=YES_NO,
        max_length=3,)

    criteria_met = models.ManyToManyField(
        TransportCriteria,
        verbose_name='What criteria has been met for transportation'
        ' support?')

    criteria_met_other = OtherCharField()

    next_visit_date = models.DateField(
        verbose_name='Visit Date for which transportation is being '
                     'planned (next visit date)',
        validators=[date_is_future, ],
        default=get_utcnow,)

    visit_facility = models.CharField(
        verbose_name='Visit facility for which transport is being '
                     'planned',
        choices=FACILITY,
        max_length=40,)

    visit_facility_other = OtherCharField()

    transport_type = models.CharField(
        verbose_name='Type of transport support being arranged',
        choices=TRANSPORT_TYPE,
        max_length=50,)

    vehicle_status = models.CharField(
        verbose_name='Status of facility vehicle arrangement at '
                     'end of transport planning encounter',
        choices=VEHICLE_ARR_STATUS,
        max_length=100,)

    transport_type_other = OtherCharField()

    vehicle_status_other = OtherCharField(
        verbose_name='If other facility vehicle status, describe '
                     'details',
        max_length=100,
        blank=True,
        null=True,)

    vehicle_request_date = models.DateField(
        verbose_name='Date of initial request for facility vehicle',
        blank=True,
        null=True,)

    facility_personnel = models.CharField(
        verbose_name='Facility transport office personnel who received '
                     'the request',
        max_length=25,
        blank=True,
        null=True,)

    bus_voucher_status = models.CharField(
        verbose_name='Status of bus voucher arrangement at end '
                     'of transport planning encounter',
        choices=BUS_VOUCHER_STATUS,
        max_length=50,)

    bus_voucher_status_other = OtherCharField(
        verbose_name='If other, describe status of transport arrangement',
        max_length=50,
        blank=True,
        null=True,)

    cash_transfer_status = models.CharField(
        verbose_name='Status of cash transfer arrangement at end '
                     'of transport planning encounter',
        choices=CASH_TRANSFER_STATUS,
        max_length=50,)

    cash_transfer_status_other = OtherCharField(
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

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Transport'
        verbose_name_plural = 'Transport'
