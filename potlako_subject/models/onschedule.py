# from django.core.exceptions import ValidationError
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OnScheduleModelMixin

# from .subject_consent import SubjectConsent
from .model_mixins import ModelCsvFormExportMixin


class Onschedule(RequiresConsentFieldsModelMixin, OnScheduleModelMixin, BaseUuidModel):

    model_csv_form_export = ModelCsvFormExportMixin

    onsite = CurrentSiteManager()

    objects = SubjectIdentifierManager()


#     @property
#     def consent_version(self):
#         return self.get_consent_version()
# 
#     def get_consent_version(self):
#         try:
#             subject_consent_obj = SubjectConsent.objects.get(
#                 subject_identifier=self.subject_identifier)
#         except SubjectConsent.DoesNotExist:
#             raise ValidationError(
#                 'Missing Consent form. Cannot proceed.')
#         else:
#             return subject_consent_obj.version
