from django.db import models
from edc_base.model_validators import date_not_future, date_is_future
from edc_base.utils import get_utcnow
from edc_protocol.validators import date_not_before_study_start

from .model_mixins import CrfModelMixin


class MissedCall(CrfModelMixin):

    entry_date = models.DateField(
        verbose_name='Date of entry',
        default=get_utcnow(),
        validators=[date_not_before_study_start, date_not_future, ],)

    notes = models.TextField(
        max_length=150,)

    repeat_call = models.DateField(
        verbose_name='When to schedule repeat call?',
        validators=[date_is_future, ],)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Call'
