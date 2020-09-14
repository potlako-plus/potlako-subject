from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import PatientCallFollowUpForm, FacilityVisitForm
from ..models import PatientCallFollowUp, FacilityVisit
from .modeladmin_mixins import CrfModelAdminMixin


class FacilityVisitInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = FacilityVisit
    form = FacilityVisitForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': [
                'interval_visit_date',
                'interval_visit_date_estimated',
                'interval_visit_date_estimation',
                'visit_facility',
                'visit_facility_other',
                'visit_reason',
                'visit_outcome', ]}
         ),)


@admin.register(PatientCallFollowUp, site=potlako_subject_admin)
class PatientCallFollowUpAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PatientCallFollowUpForm
    inlines = [FacilityVisitInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'encounter_date',
                       'start_time',
                       'patient_info_change',
                       'first_specialist_visit',
                       'perfomance_status',
                       'pain_score',
                       'new_complaints',
                       'new_complaints_description',
                       'interval_visit',
                       'facility_visited_count',
                       'last_visit_date',
                       'last_visit_date_estimated',
                       'last_visit_date_estimation',
                       'last_visit_facility',
                       'appt_change',
                       'appt_change_reason',
                       'appt_change_reason_other',
                       'investigations_ordered',
                       'transport_support',
                       'next_appointment_date',
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'transport_support_received',
                       'transport_details',
                       'sms_received',
                       'sms_outcome',
                       'sms_outcome_other',
                       'clinician_communication_issues',
                       'clinician_issues_details',
                       'communication_issues',
                       'issues_details',
                       'other_issues',
                       'other_issues_details',
                       'call_achievements',
                       'call_achievements_other',
                       'medical_evaluation_understanding',
                       'next_step_understanding',
                       'additional_comments',
                       'patient_followup_end_time',
                       'encounter_duration',
                       ),
        }), audit_fieldset_tuple
    )

    radio_fields = {'patient_info_change': admin.VERTICAL,
                    'first_specialist_visit': admin.VERTICAL,
                    'perfomance_status': admin.VERTICAL,
                    'pain_score': admin.VERTICAL,
                    'new_complaints': admin.VERTICAL,
                    'interval_visit': admin.VERTICAL,
                    'last_visit_date_estimated': admin.VERTICAL,
                    'last_visit_date_estimation': admin.VERTICAL,
                    'appt_change': admin.VERTICAL,
                    'appt_change_reason': admin.VERTICAL,
                    'investigations_ordered': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'next_ap_facility': admin.VERTICAL,
                    'transport_support_received': admin.VERTICAL,
                    'clinician_communication_issues': admin.VERTICAL,
                    'communication_issues': admin.VERTICAL,
                    'other_issues': admin.VERTICAL,
                    'medical_evaluation_understanding': admin.VERTICAL,
                    'sms_received': admin.VERTICAL,
                    'sms_outcome': admin.VERTICAL,
                    }

    filter_horizontal = ('call_achievements',)

    readonly_fields = ('encounter_duration',)
