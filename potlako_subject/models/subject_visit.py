import csv
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager as BaseCurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.constants import NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin
from edc_appointment.models import Appointment

from ..choices import VISIT_INFO_SOURCE, VISIT_UNSCHEDULED_REASON, VISIT_REASON


class ModelCsvFormExportMixin:

    def __init__(self, model=None):
        self.model = model

    @property
    def fields_verbose_names(self):
        """Return a list of list of field and verbose name.
        """
        exclude_list = [
            'created', 'id', 'device_created', 'device_modified',
            'modified', 'user_created', 'user_modified', 'hostname_created',
            'hostname_modified', 'revision']
        f_list = [
            [field.name, self.model._meta.get_field(field.name).verbose_name]
            for field in self.model._meta.fields if field.name not in exclude_list]
        header = [['Field name', 'Questionnaire']]
        field_list = header + f_list
        return field_list

    @property
    def export_from_as_csv(self):

        with open(self.model._meta.label_lower + '.csv', "w+") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.fields_verbose_names)


class CurrentSiteManager(VisitModelManager, BaseCurrentSiteManager):
    pass


class SubjectVisit(VisitModelMixin, ReferenceModelMixin, CreatesMetadataModelMixin,
                   SiteModelMixin, RequiresConsentFieldsModelMixin, BaseUuidModel):

    """A model completed by the user that captures the covering
    information for the data collected for this timepoint/appointment,
    e.g.report_datetime.
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    reason = models.CharField(
        verbose_name='What is the reason for this visit report?',
        max_length=25,
        choices=VISIT_REASON)

    reason_unscheduled = models.CharField(
        verbose_name=(
            'If \'Unscheduled\' above, provide reason for '
            'the unscheduled visit'),
        max_length=50,
        choices=VISIT_UNSCHEDULED_REASON,
        default=NOT_APPLICABLE)

    info_source = models.CharField(
        verbose_name='What is the main source of this information?',
        max_length=40,
        choices=VISIT_INFO_SOURCE)

    on_site = CurrentSiteManager()

    objects = VisitModelManager()

    class Meta(VisitModelMixin.Meta):
        pass
