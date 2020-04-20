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
         ), audit_fieldset_tuple)


@admin.register(PatientCallFollowUp, site=potlako_subject_admin)
class PatientCallFollowUpAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PatientCallFollowUpForm
    inlines = [FacilityVisitInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'encounter_date',
                       'start_time',
                       'patient_residence_change',
                       'phone_number_change',
                       'next_kin_contact_change',
                       'perfomance_status',
                       'pain_score',
                       'new_complaints',
                       'new_complaints_description',
                       'interval_visit',
                       'facility_visited_count',
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
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'transport_support_received',
                       'transport_details',
                       'clinician_communication_issues',
                       'clinician_issues_details',
                       'communication_issues',
                       'issues_details',
                       'other_issues',
                       'other_issues_details',
                       'call_achievements',
                       'medical_evaluation_understanding',
                       'next_step_understanding',
                       'sms_received',
                       'additional_comments',
                       'patient_followup_end_time',
                       'encounter_duration',
                       ),
        }), audit_fieldset_tuple
    )

    radio_fields = {'patient_residence_change': admin.VERTICAL,
                    'phone_number_change': admin.VERTICAL,
                    'next_kin_contact_change': admin.VERTICAL,
                    'new_complaints': admin.VERTICAL,
                    'interval_visit': admin.VERTICAL,
                    'investigation_ordered': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'next_visit_delayed': admin.VERTICAL,
                    'visit_delayed_reason': admin.VERTICAL,
                    'patient_factor': admin.VERTICAL,
                    'health_system_factor': admin.VERTICAL,
                    'next_ap_facility': admin.VERTICAL,
                    'transport_support_received': admin.VERTICAL,
                    'clinician_communication_issues': admin.VERTICAL,
                    'communication_issues': admin.VERTICAL,
                    'other_issues': admin.VERTICAL,
                    'medical_evaluation_understanding': admin.VERTICAL,
                    'sms_received': admin.VERTICAL
                    }

    filter_horizontal = ('call_achievements',)

    readonly_fields = ('encounter_duration',)
