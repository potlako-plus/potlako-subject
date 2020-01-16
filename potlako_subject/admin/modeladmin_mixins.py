from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminAuditFieldsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin, ModelAdminReadOnlyMixin,
    ModelAdminRedirectOnDeleteMixin)


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
