from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import date_is_future
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager, SiteModelMixin

from .model_mixins import CrfModelMixin


class MissedCallRecordManager(models.Manager):

    def get_by_natural_key(self, repeat_call, missed_call):
        return self.get(missed_call=missed_call,
                        repeat_call=repeat_call)


class MissedCall(CrfModelMixin):
    
    is_complete = models.BooleanField(
        null=True,
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Call'
        
class MissedCallRecord(SiteModelMixin, BaseUuidModel):
    
    missed_call = models.ForeignKey(MissedCall, on_delete=PROTECT)
    
    notes = models.TextField(
        max_length=150,)

    repeat_call = models.DateField(
        verbose_name='Scheduled date for repeat call',
        validators=[date_is_future, ],)
    
    history = HistoricalRecords()
    
    on_site = CurrentSiteManager()
    
    objects = MissedCallRecordManager()
    
    def natural_key(self):
        return (self.repeat_call, ) + self.missed_call.natural_key()
    natural_key.dependencies = ['potlako_subject.missedcall']
    
    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Missed Call Record'
        unique_together = ('missed_call', 'repeat_call')
        
