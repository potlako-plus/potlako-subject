from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import InvestigationsOrderedForm, LabTestForm
from ..models import InvestigationsOrdered, LabTest
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


@admin.register(InvestigationsOrdered, site=potlako_subject_admin)
class InvestigationsOrderedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InvestigationsOrderedForm

    inlines = [LabTestInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'tests_ordered_type',
                       'tests_ordered_type_other',
                       'pathology_test',
                       'pathology_test_other',
                       'pathology_specimen_date',
                       'pathology_nhl_date',
                       'biopsy_specify',
                       'fna_location',
                       'imaging_test_type',
                       'xray_tests',
                       'ultrasound_tests',
                       'ct_tests',
                       'mri_tests',
                       'imaging_tests_type_other',
                       'facility_ordered',
                       'facility_ordered_other',
                       'ordered_date',
                       'ordered_date_estimated',
                       'ordered_date_estimation',
                       'specimen_tracking_notes',),
        }), audit_fieldset_tuple)

    radio_fields = {'ordered_date_estimated': admin.VERTICAL,
                    'ordered_date_estimation': admin.VERTICAL}

    filter_horizontal = ('tests_ordered_type', 'pathology_test', 'imaging_test_type')
