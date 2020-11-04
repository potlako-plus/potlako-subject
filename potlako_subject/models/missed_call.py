from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_validators import date_is_future
from edc_base.model_mixins import BaseUuidModel

from .model_mixins import CrfModelMixin


class MissedCall(CrfModelMixin):
    
    is_complete = models.BooleanField(
        null=True,
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Call'
        
class MissedCallRecord(BaseUuidModel):
    
    missed_call = models.ForeignKey(MissedCall, on_delete=PROTECT)
    
    notes = models.TextField(
        max_length=150,)

    repeat_call = models.DateField(
        verbose_name='Scheduled date for repeat call',
        validators=[date_is_future, ],)
    
    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Call Record'
