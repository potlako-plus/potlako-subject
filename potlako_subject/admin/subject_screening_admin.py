from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fields, audit_fieldset_tuple)

from ..admin_site import potlako_subject_admin
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter


@admin.register(SubjectScreening, site=potlako_subject_admin)
class SubjectScreeningAdmin(
        ModelAdminMixin, admin.ModelAdmin):

    form = SubjectScreeningForm

    fieldsets = (
        (None, {
            'fields': (
                'screening_identifier',
                'enrollment_interest',
                'disinterest_reason',
                'disinterest_reason_other',
                'residency',
                'nationality',
                'age_in_years',
                'has_diagnosis',
                'enrollment_site',
                'enrollment_site_other'
            )}),
        audit_fieldset_tuple)

    search_fields = ('subject_identifier',)

    radio_fields = {
        'residency': admin.VERTICAL,
        'nationality': admin.VERTICAL,
        'has_diagnosis': admin.VERTICAL,
        'enrollment_interest': admin.VERTICAL,
        'disinterest_reason': admin.VERTICAL, }

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) + audit_fields +
                ('age_in_years',))
