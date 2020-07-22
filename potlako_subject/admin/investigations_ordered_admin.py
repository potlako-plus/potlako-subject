from django.contrib import admin
from edc_model_admin import TabularInlineMixin

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
                       'report_datetime',
                       'tests_ordered_type',
                       'tests_ordered_type_other',
                       'facility_ordered',
                       'facility_ordered_other',
                       'ordered_date',
                       'ordered_date_estimated',
                       'ordered_date_estimation',
                       'pathology_test',
                       'biopsy_specify',
                       'fna_location',
                       'pathology_specimen_date',
                       'imaging_test_status',
                       'imaging_test_type',
                       'xray_tests',
                       'ultrasound_tests',
                       'ct_tests',
                       'mri_tests',
                       'imaging_tests_type_other',
                       'imaging_tests_date'),
        }),
    )

    radio_fields = {'tests_ordered_type': admin.VERTICAL,
                    'facility_ordered': admin.VERTICAL,
                    'ordered_date_estimated': admin.VERTICAL,
                    'ordered_date_estimation': admin.VERTICAL,
                    'imaging_test_status': admin.VERTICAL,
                    'imaging_test_type': admin.VERTICAL}

    filter_horizontal = ('pathology_test',)
