from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from ..admin_site import potlako_subject_admin
from ..forms import PatientCallInitialForm
from ..models import PatientCallInitial


@admin.register(PatientCallInitial, site=potlako_subject_admin)
class PatientCallInitialAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    form = PatientCallInitialForm

    fieldsets = (
        (None, {
            'fields': ('patient_call_date',
                       'patient_call_time',
                       'start_time',
                       'dob_known',
                       'dob',
                       'patient_contact_residence_change',
                       'residential_district',
                       'patient_village',
                       'patient_kgotla',
                       'primary_clinic',
                       'patient_contact_change',
                       'patient_number',
                       'next_of_kin',
                       'next_kin_contact_change',
                       'primary_keen_contact',
                       'secondary_keen_contact',
                       'patient_symptoms',
                       'patient_symptoms_date',
                       'other_facility',
                       'facility_number',
                       'facility_previously_visited',
                       'previous_facility_period',
                       'perfomance_status',
                       'pain_score',
                       'hiv_status',
                       'hiv_test_date_known',
                       'hiv_test_date',
                       'cancer_suspicion_known',
                       'enrollment_clinic_visit_method',
                       'slh_travel',
                       'tests_ordered',
                       'tests_type',
                       'tests_type_other',
                       'biospy_part',
                       'next_appointment_date',
                       'next_visit_delayed',
                       'visit_delayed_count',
                       'visit_delayed_reason',
                       'patient_factor',
                       'patient_factor_other',
                       'health_system_factor',
                       'health_system_factor_other',
                       'delayed_visit_description',
                       'next_appointment_facility',
                       'next_appointment_facility_unit',
                       'next_appointment_facility_unit_other',
                       'patient_understanding',
                       'transport_support',
                       'call_achievements',
                       'clinician_information',
                       'comments',
                       'cancer_probability',
                       'encounter_end_time',
                       'initial_call_end_time',
                       'call_duration'
                       ),
        }),
    )

    radio_fields = {'dob_known': admin.VERTICAL,
                    'patient_contact_residence_change': admin.VERTICAL,
                    'residential_district': admin.VERTICAL,
                    'primary_clinic': admin.VERTICAL,
                    'patient_contact_change': admin.VERTICAL,
                    'next_of_kin': admin.VERTICAL,
                    'next_kin_contact_change': admin.VERTICAL,
                    'other_facility': admin.VERTICAL,
                    'facility_previously_visited': admin.VERTICAL,
                    'hiv_status': admin.VERTICAL,
                    'hiv_test_date_known': admin.VERTICAL,
                    'cancer_suspicion_known': admin.VERTICAL,
                    'tests_ordered': admin.VERTICAL,
                    'tests_type': admin.VERTICAL,
                    'next_visit_delayed': admin.VERTICAL,
                    'visit_delayed_reason': admin.VERTICAL,
                    'patient_factor': admin.VERTICAL,
                    'health_system_factor': admin.VERTICAL,
                    'next_appointment_facility': admin.VERTICAL,
                    'next_appointment_facility_unit': admin.VERTICAL,
                    'patient_understanding': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'clinician_information': admin.VERTICAL,
                    'cancer_probability': admin.VERTICAL,
                    }

    filter_horizontal = ('call_achievements',)
