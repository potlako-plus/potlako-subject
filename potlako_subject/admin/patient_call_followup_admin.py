from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import PatientCallFollowUpForm
from ..models import PatientCallFollowUp


@admin.register(PatientCallFollowUp, site=potlako_subject_admin)
class PatientCallFollowUpAdmin(admin.ModelAdmin):

    form = PatientCallFollowUpForm

    fieldsets = (
        (None, {
            'fields': ('coordinator_encounter_date',
                       'start_time',
                       'encounter_duration',
                       'patient_residence_change',
                       'patient_district',
                       'patient_village',
                       'patient_kgotla',
                       'phone_number_change',
                       'patient_number',
                       'next_kin_contact_change',
                       'primary_keen_contact',
                       'secondary_keen_contact',
                       'perfomance_status',
                       'pain_score',
                       'new_complaints',
                       'new_complaints_description',
                       'interval_visit',
                       'interval_visit_date',
                       'visit_facility',
                       'visit_reason',
                       'visit_outcome',
                       'investigation_ordered',
                       'transport_support',
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
                       'patient_understanding',
                       'transport_support_received',
                       'transport_details',
                       'clinician_communication_issues',
                       'clinician_issues_details',
                       'coordinator_communication_issues',
                       'coordinator_issues_details',
                       'other_issues',
                       'other_issues_details',
                       'call_achievements',
                       'medical_evaluation_understanding',
                       'next_step_understanding',
                       'sms_received',
                       'additional_comments',
                       'patient_followup_end_time'
                       ),
        }),
    )

    radio_fields = {'patient_residence_change': admin.VERTICAL,
                    'patient_district': admin.VERTICAL,
                    'phone_number_change': admin.VERTICAL,
                    'next_kin_contact_change': admin.VERTICAL,
                    'new_complaints': admin.VERTICAL,
                    'interval_visit': admin.VERTICAL,
                    'visit_facility': admin.VERTICAL,
                    'visit_outcome': admin.VERTICAL,
                    'investigation_ordered': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'next_visit_delayed': admin.VERTICAL,
                    'visit_delayed_reason': admin.VERTICAL,
                    'patient_factor': admin.VERTICAL,
                    'health_system_factor': admin.VERTICAL,
                    'next_appointment_facility': admin.VERTICAL,
                    'patient_understanding': admin.VERTICAL,
                    'transport_support_received': admin.VERTICAL,
                    'clinician_communication_issues': admin.VERTICAL,
                    'coordinator_communication_issues': admin.VERTICAL,
                    'other_issues': admin.VERTICAL,
                    'medical_evaluation_understanding': admin.VERTICAL,
                    'sms_received': admin.VERTICAL
                    }

    filter_horizontal = ('call_achievements',)
