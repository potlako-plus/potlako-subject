from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import InvestigationsResultedForm
from ..models import InvestigationsResulted
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(InvestigationsResulted, site=potlako_subject_admin)
class InvestigationsResultedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InvestigationsResultedForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'tests_resulted_type',
                       'imaging_tests',
                       'pathology_received_date',
                       'pathology_communicated_date',
                       'imaging_tests_date',
                       'diagnosis_results',
                       'diagnosis_results_other',
                       'cancer_type',
                       'diagnoses_made',),
        }), audit_fieldset_tuple)

    radio_fields = {'diagnosis_results': admin.VERTICAL, }

    filter_horizontal = ('tests_resulted_type',)
