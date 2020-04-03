from django.contrib import admin
from edc_model_admin import TabularInlineMixin

from ..admin_site import potlako_subject_admin
from ..forms import InvestigationsForm, LabTestForm
from ..models import Investigations, LabTest
from .modeladmin_mixins import CrfModelAdminMixin


class LabTestInlineAdmin(TabularInlineMixin, admin.TabularInline):

    model = LabTest
    form = LabTestForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'lab_test_type',
                'lab_test_date',
                'lab_test_type_other',
                'lab_test_status',
                'lab_test_status_other')}
         ),)


@admin.register(Investigations, site=potlako_subject_admin)
class InvestigationsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InvestigationsForm

    inlines = [LabTestInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'facility_ordered',
                       'facility_ordered_other',
                       'ordered_date',
                       'lab_tests_ordered',
                       'pathology_tests_ordered',
                       'pathology_test',
                       'biopsy_other',
                       'fna_location',
                       'pathology_specimen_date',
                       'pathology_nhl_date',
                       'pathology_result_date',
                       'pathology_received_date',
                       'pathology_communicated_date',
                       'imaging_tests',
                       'imaging_test_status',
                       'imaging_test_type',
                       'ultrasound_tests_other',
                       'imaging_tests_other',
                       'imaging_tests_date',
                       'specimen_tracking_notes',
                       'diagnosis_results',
                       'cancer_type',
                       'diagnoses_made',
                       'cancer_stage',
                       'cancer_stage_other',
                       'bpcc_enrolled',
                       'bpcc_identifier',
                       'end_time'),
        }),
    )

    radio_fields = {'facility_ordered': admin.VERTICAL,
                    'lab_tests_ordered': admin.VERTICAL,
                    'pathology_tests_ordered': admin.VERTICAL,
                    'pathology_test': admin.VERTICAL,
                    'imaging_tests': admin.VERTICAL,
                    'imaging_test_status': admin.VERTICAL,
                    'imaging_test_type': admin.VERTICAL,
                    'diagnosis_results': admin.VERTICAL,
                    'cancer_stage': admin.VERTICAL,
                    'bpcc_enrolled': admin.VERTICAL}
