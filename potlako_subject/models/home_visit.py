from django.apps import apps as django_apps
from django.db import models
from django.db.models import Q
from edc_action_item.models import ActionItem
from edc_action_item.site_action_items import site_action_items
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_is_future
from edc_constants.constants import DEAD
from edc_constants.constants import NEW

from potlako_prn.action_items import DEATH_REPORT_ACTION, COORDINATOR_EXIT_ACTION

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
        max_length=40,
        blank=True,
        null=True)

    clinician_facility_other = OtherCharField()

    visit_outcome = models.CharField(
        verbose_name='Outcome of home visit',
        choices=ALIVE_DEAD_LTFU,
        max_length=30,
        help_text=('(IF DIED, COMPLETE \'DEATH FORM\'.'
                   'IF LTFU,COMPLETE \'EXIT FORM\')'))

    visit_outcome_other = OtherCharField()

    next_appointment = models.DateField(
        verbose_name='If alive, next appointment date',
        validators=[date_is_future, ],
        blank=True,
        null=True,)

    next_ap_facility = models.CharField(
        verbose_name='If alive, next appointment facility',
        choices=FACILITY,
        max_length=40,
        blank=True,
        null=True,)

    next_ap_facility_other = OtherCharField()

    next_ap_type = models.CharField(
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.visit_outcome == DEAD:
            self.trigger_action_item(DEATH_REPORT_ACTION, COORDINATOR_EXIT_ACTION)
        elif self.visit_outcome == 'ltfu':
            self.trigger_action_item(COORDINATOR_EXIT_ACTION, DEATH_REPORT_ACTION)
        else:
            action_items = ActionItem.objects.filter(
                Q(action_type__name=COORDINATOR_EXIT_ACTION) |
                Q(action_type__name=DEATH_REPORT_ACTION),
                subject_identifier=self.subject_visit.appointment.subject_identifier,
                status=NEW)
            for action in action_items:
                action.delete()

    def trigger_action_item(self, action_name, delete_action):

        try:
            coordinator_action = ActionItem.objects.get(
                action_type__name=delete_action,
                subject_identifier=self.subject_visit.appointment.subject_identifier,
                status=NEW)
        except ActionItem.DoesNotExist:
            pass
        else:
            coordinator_action.delete()

        try:
            ActionItem.objects.get(
                action_type__name=delete_action,
                subject_identifier=self.subject_visit.appointment.subject_identifier,
                status=NEW)
        except ActionItem.DoesNotExist:
            action_cls = site_action_items.get(action_name)
            action_cls(subject_identifier=
                       self.subject_visit.appointment.subject_identifier)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Home Visit'
