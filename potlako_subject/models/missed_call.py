from django.db import models
from edc_base.model_validators import date_is_future

from .model_mixins import CrfModelMixin


class MissedCall(CrfModelMixin):

    notes = models.TextField(
        max_length=150,)

    repeat_call = models.DateField(
        verbose_name='Scheduled date for repeat call',
        validators=[date_is_future, ],)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Call'
