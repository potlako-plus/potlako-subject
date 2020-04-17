from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_is_future

from ..choices import ALIVE_DEAD_LTFU, CLINICIAN_TYPE, FACILITY, VISIT_TYPE
from .model_mixins import CrfModelMixin


class HomeVisit(CrfModelMixin):

    clinician_type = models.CharField(
        verbose_name='Type of clinician who made the home visit',
        choices=CLINICIAN_TYPE,
        max_length=50)

    clinician_type_other = OtherCharField()

    clinician_facility = models.CharField(
        verbose_name='Name of facility where clinician1 works',
        choices=FACILITY,
        max_length=30)

    clinician_facility_other = OtherCharField()

    visit_outcome = models.CharField(
        verbose_name='Outcome of home visit',
        choices=ALIVE_DEAD_LTFU,
        max_length=30,
        help_text='(IF DIED OR LTFU, COMPLETE \'EXIT FORM\')')

    visit_outcome_other = OtherCharField()

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

    next_ap_facility_other = OtherCharField()

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

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Home Visit'
