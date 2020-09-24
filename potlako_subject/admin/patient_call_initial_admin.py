from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fields, audit_fieldset_tuple)

from ..admin_site import potlako_subject_admin
from ..forms import PatientCallInitialForm, PreviousFacilityVisitForm
from ..models import PatientCallInitial, PreviousFacilityVisit
from .modeladmin_mixins import CrfModelAdminMixin


class FacilityVisitInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = PreviousFacilityVisit
    form = PreviousFacilityVisitForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': [
                'facility_visited',
                'facility_visited_other',
                'previous_facility_period', ]}
         ),)


@admin.register(PatientCallInitial, site=potlako_subject_admin)
class PatientCallInitialAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PatientCallInitialForm
    inlines = [FacilityVisitInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'patient_call_date',
                       'patient_call_time',
                       'age_in_years',
                       'residential_district',
                       'residential_district_other',
                       'patient_kgotla',
                       'primary_clinic',
                       'primary_clinic_other',
                       'education_level',
                       'heard_of_potlako',
                       'source_of_info',
                       'source_of_info_other',
                       'potlako_sms_received',
                       'sms_platform',
                       'sms_platform_other',
                       'work_status',
                       'work_type',
                       'work_type_other',
                       'unemployed_reason',
                       'unemployed_reason_other',
                       'social_welfare',
                       'medical_conditions',
                       'patient_residence',
                       'patient_residence_other',
                       'patient_info_change',
                       'patient_symptoms',
                       'patient_symptoms_date',
                       'patient_symptoms_date_estimated',
                       'patient_symptoms_date_estimation',
                       'symptoms_duration_report',
                       'symptoms_duration',
                       'other_facility',
                       'facility_number',
                       'perfomance_status',
                       'pain_score',
                       'hiv_status',
                       'hiv_test_date',
                       'hiv_test_date_estimated',
                       'hiv_test_date_estimation',
                       'cancer_suspicion_known',
                       'enrollment_visit_method',
                       'enrollment_visit_method_other',
                       'slh_travel',
                       'tests_ordered',
                       'next_appointment_date',
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'next_ap_facility_unit',
                       'next_ap_facility_unit_other',
                       'transport_support',
                       'comments',
                       'initial_call_end_time',
                       'call_duration'
                       ),
        }),
        audit_fieldset_tuple
    )

    radio_fields = {'education_level': admin.VERTICAL,
                    'heard_of_potlako': admin.VERTICAL,
                    'source_of_info': admin.VERTICAL,
                    'potlako_sms_received': admin.VERTICAL,
                    'work_status': admin.VERTICAL,
                    'work_type': admin.VERTICAL,
                    'unemployed_reason': admin.VERTICAL,
                    'social_welfare': admin.VERTICAL,
                    'medical_conditions': admin.VERTICAL,
                    'patient_info_change': admin.VERTICAL,
                    'patient_symptoms_date_estimated': admin.VERTICAL,
                    'patient_symptoms_date_estimation': admin.VERTICAL,
                    'symptoms_duration': admin.VERTICAL,
                    'other_facility': admin.VERTICAL,
                    'hiv_status': admin.VERTICAL,
                    'hiv_test_date_estimated': admin.VERTICAL,
                    'hiv_test_date_estimation': admin.VERTICAL,
                    'cancer_suspicion_known': admin.VERTICAL,
                    'enrollment_visit_method': admin.VERTICAL,
                    'tests_ordered': admin.VERTICAL,
                    'next_ap_facility_unit': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'perfomance_status': admin.VERTICAL,
                    'pain_score': admin.VERTICAL,
                    }

    filter_horizontal = ('sms_platform', 'patient_residence',)

    readonly_fields = ('call_duration',)

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) + ('age_in_years',) + audit_fields)

