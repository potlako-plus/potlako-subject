from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.modeladmin_mixins import FormAsJSONModelAdminMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_model_admin import (
    ModelAdminAuditFieldsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin, ModelAdminReadOnlyMixin,
    ModelAdminRedirectOnDeleteMixin)
from ..models.model_mixins import BaselineRoadMapMixin
from edc_metadata import NextFormGetter
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)


class ModelAdminMixin(
        ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
        ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
        ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
        ModelAdminInstitutionMixin, ModelAdminRedirectOnDeleteMixin,
        ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter
    extra_context_models = None

    def add_view(self, request, form_url='', extra_context=None):

        extra_context = extra_context or {}
        if self.extra_context_models:
            extra_context_dict = BaselineRoadMapMixin(
                subject_identifier=request.GET.get(
                    'subject_identifier')).baseline_dict
            [extra_context.update({key: extra_context_dict.get(key)})for key in self.extra_context_models]
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        if self.extra_context_models:
            extra_context_dict = BaselineRoadMapMixin(
                subject_identifier=request.GET.get(
                    'subject_identifier')).baseline_dict
            [extra_context.update({key: extra_context_dict.get(key)})for key in self.extra_context_models]
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin,
                         ModelAdminMixin,
                         FieldsetsModelAdminMixin,
                         FormAsJSONModelAdminMixin,
                         admin.ModelAdmin):

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. '
        'Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(
            subject_identifier=obj.subject_identifier,
            appointment=str(obj.subject_visit.appointment.id))

    def view_on_site(self, obj):
        dashboard_url_name = settings.DASHBOARD_URL_NAMES.get(
            'subject_dashboard_url')
        try:
            url = reverse(
                dashboard_url_name, kwargs=dict(
                    subject_identifier=obj.subject_visit.subject_identifier,
                    appointment=str(obj.subject_visit.appointment.id)))
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url
