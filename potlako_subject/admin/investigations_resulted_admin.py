from django.contrib import admin

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
                       'report_datetime',
                       'tests_resulted_type',
                       'tests_resulted_type_other',
                       'pathology_specimen_date',
                       'pathology_nhl_date',
                       'pathology_result_date',
                       'pathology_received_date',
                       'pathology_communicated_date',
                       'imaging_tests_date',
                       'specimen_tracking_notes',
                       'diagnosis_results',
                       'diagnosis_results_other',
                       'cancer_type',
                       'diagnoses_made',
                       'cancer_stage',),
        }),
    )

    radio_fields = {'tests_resulted_type': admin.VERTICAL,
                    'diagnosis_results': admin.VERTICAL,
                    'cancer_stage': admin.VERTICAL}
