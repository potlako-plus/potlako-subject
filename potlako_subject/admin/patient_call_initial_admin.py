from django.contrib import admin
from ..admin_site import potlako_subject_admin
from ..forms import PatientCallInitialForm
from ..models import PatientCallInitial

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PatientCallInitial, site=potlako_subject_admin)
class PatientCallInitialAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PatientCallInitialForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'patient_call_date',
                       'patient_call_time',
                       'age_in_years',
                       'residential_district',
                       'patient_kgotla',
                       'primary_clinic',
                       'primary_clinic_other',
                       'patient_contact_change',
                       'patient_number',
                       'next_of_kin',
                       'next_kin_contact_change',
                       'primary_keen_contact',
                       'secondary_keen_contact',
                       'patient_symptoms',
                       'patient_symptoms_date',
                       'patient_symptoms_date_estimated',
                       'patient_symptoms_date_estimation',
                       'symptoms_duration_report',
                       'symptoms_duration',
                       'other_facility',
                       'facility_number',
                       'facility_visited',
                       'facility_visited_other',
                       'previous_facility_period',
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
                       'tests_type',
                       'tests_type_other',
                       'biospy_part',
                       'next_appointment_date',
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'next_ap_facility_unit',
                       'next_ap_facility_unit_other',
                       'transport_support',
                       'call_achievements',
                       'call_achievements_other',
                       'comments',
                       'cancer_probability',
                       'initial_call_end_time',
                       'call_duration'
                       ),
        }),
    )

    radio_fields = {'residential_district': admin.VERTICAL,
                    'primary_clinic': admin.VERTICAL,
                    'patient_contact_change': admin.VERTICAL,
                    'next_of_kin': admin.VERTICAL,
                    'patient_symptoms_date_estimated': admin.VERTICAL,
                    'patient_symptoms_date_estimation': admin.VERTICAL,
                    'symptoms_duration': admin.VERTICAL,
                    'next_kin_contact_change': admin.VERTICAL,
                    'other_facility': admin.VERTICAL,
                    'hiv_status': admin.VERTICAL,
                    'hiv_test_date_estimated': admin.VERTICAL,
                    'hiv_test_date_estimation': admin.VERTICAL,
                    'cancer_suspicion_known': admin.VERTICAL,
                    'enrollment_visit_method': admin.VERTICAL,
                    'tests_ordered': admin.VERTICAL,
                    'next_ap_facility': admin.VERTICAL,
                    'next_ap_facility_unit': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'cancer_probability': admin.VERTICAL,
                    }

    filter_horizontal = ('call_achievements',
                         'facility_visited',
                         'tests_type')

    readonly_fields = ('call_duration',)
