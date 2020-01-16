from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OnScheduleModelMixin


class Onschedule(OnScheduleModelMixin, BaseUuidModel):

    onsite = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()
