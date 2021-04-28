from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_base.model_validators import date_is_future, date_not_future

from ..choices import DONE_NOT_DONE


class EvaluationTimelineManager(models.Manager):

    def get_by_natural_key(self, navigation_plan, key_step, target_date):
        return self.get(navigation_plan=navigation_plan,
                        key_step=key_step,
                        target_date=target_date)


class NavigationSummaryAndPlan(UniqueSubjectIdentifierFieldMixin,
                               SiteModelMixin, BaseUuidModel):

    diagnostic_plan = models.TextField(
        max_length=1000)

    notes = models.TextField(
        verbose_name='Notes',
        max_length=1000,
        null=True,
        blank=True)

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Navigation Plan And Summary'
        verbose_name_plural = 'Navigation Plan And Summaries'


class EvaluationTimeline(SiteModelMixin, BaseUuidModel):
    """ Inline Evalaution timeline to capture all key milestones """

    navigation_plan = models.ForeignKey(NavigationSummaryAndPlan, on_delete=PROTECT)

    key_step = models.CharField(
        verbose_name='Key step',
        max_length=50,)

    target_date = models.DateField(
        verbose_name='Target Date',)

    adjusted_target_date = models.DateField(
        verbose_name='Adjusted Target Date',
        blank=True,
        null=True)

    key_step_status = models.CharField(
        verbose_name='Key step status',
        max_length=8,
        choices=DONE_NOT_DONE)

    completion_date = models.DateField(
        verbose_name='Achieved date',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text='or date determined not required'
    )

    review_required = models.CharField(
        verbose_name='Requires multidisiciplinary review?',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = EvaluationTimelineManager()

    def natural_key(self):
        return (self.key_step, self.target_date,) + self.navigation_plan.natural_key()

    natural_key.dependencies = ['potlako_subject.navigationsummaryandplan']

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Evaluation Timeline'
        unique_together = ('navigation_plan', 'key_step', 'target_date')
