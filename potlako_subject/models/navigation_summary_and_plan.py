from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_is_future, date_not_future
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..choices import DONE_NOT_DONE


class NavigationPlanAndSummary(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ],
        help_text='Date and time of report.')

    diagnostic_plan = models.TextField(
        max_length=500)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Navigation Plan And Summary'
        verbose_name_plural = 'Navigation Plan And Summaries'


class EvaluationTimeline(BaseUuidModel):
    """ Inline Evalauttion timeline to capture all key milestones """

    navigation_plan = models.ForeignKey(NavigationPlanAndSummary, on_delete=PROTECT)

    key_step = models.CharField(
        verbose_name='Key step',
        max_length=50,)

    target_date = models.DateField(
        verbose_name='Target Date',
        validators=[date_is_future])

    key_step_status = models.CharField(
        verbose_name='Key step status',
        max_length=8,
        choices=DONE_NOT_DONE)

    completion_date = models.DateField(
        verbose_name='Achieved date',
        validators=[date_not_future],
        help_text='or date determined not required'
    )

    review_required = models.CharField(
        verbose_name='Required multidisiciplinary review?',
        max_length=3,
        choices=YES_NO)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Evaluiation Timeline'
        unique_together = ('navigation_plan', 'key_step', 'target_date')
