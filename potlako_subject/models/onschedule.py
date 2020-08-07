from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OnScheduleModelMixin


class Onschedule(
        RequiresConsentFieldsModelMixin, OnScheduleModelMixin, BaseUuidModel):

    onsite = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    def save(self, *args, **kwargs):
        self.consent_version = None
        super().save(*args, **kwargs)
