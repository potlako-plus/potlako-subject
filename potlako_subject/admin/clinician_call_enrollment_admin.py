from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fields, audit_fieldset_tuple)

from ..admin_site import potlako_subject_admin
from ..forms import ClinicianCallEnrollmentForm
from ..models import ClinicianCallEnrollment
from .subject_screening_admin import ModelAdminMixin


@admin.register(ClinicianCallEnrollment, site=potlako_subject_admin)
class ClinicianCallEnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicianCallEnrollmentForm

    fieldsets = (
        (None, {
            'fields': ('reg_date',
                       'report_datetime',
                       'screening_identifier',
                       'record_id',
                       'info_from_clinician',
                       'call_clinician',
                       'info_source_specify',
                       'call_clinician_type',
                       'call_clinician_other',
                       'consented_contact',
                       'received_training',
                       'facility',
                       'facility_unit',
                       'unit_other',
                       'national_identity',
                       'hospital_identity',
                       'clinician_name',
                       'clinician_type',
                       'clinician_other',
                       'symptoms',
                       'symptoms_other',
                       'early_symptoms_date',
                       'symptoms_details',
                       'suspected_cancer',
                       'suspicion_level',
                       'performance',
                       'pain_score',
                       'last_hiv_result',
                       'patient_disposition',
                       'referral_reason',
                       'referral_date',
                       'referral_facility',
                       'referral_unit',
                       'referral_discussed',
                       'referral_name',
                       'referral_fu',
                       'referral_fu_date',
                       'triage_status',
                       'investigated',
                       'notes',
                       'vehicle_req',
                       'paper_register',
                       'comments',
                       )
        }),
        ('Personal Details', {
            'fields': ('last_name',
                       'first_name',
                       'dob',
                       'age_in_years',
                       'gender',
                       'village_town',
                       'kgotla',
                       'nearest_facility',
                       'primary_cell',
                       'secondary_cell',
                       'kin_lastname',
                       'kin_firstname',
                       'kin_relationship',
                       'kin_relation_other',
                       'kin_cell',
                       'other_kin_avail',
                       'other_kin_lastname',
                       'other_kin_firstname',
                       'other_kin_rel',
                       )
        }),
        audit_fieldset_tuple
    )

    radio_fields = {'info_from_clinician': admin.VERTICAL,
                    'call_clinician_type': admin.VERTICAL,
                    'consented_contact': admin.VERTICAL,
                    'received_training': admin.VERTICAL,
                    'facility': admin.VERTICAL,
                    'facility_unit': admin.VERTICAL,
                    'gender': admin.VERTICAL,
                    'nearest_facility': admin.VERTICAL,
                    'kin_relationship': admin.VERTICAL,
                    'other_kin_avail': admin.VERTICAL,
                    'other_kin_rel': admin.VERTICAL,
                    'clinician_type': admin.VERTICAL,
                    'suspected_cancer': admin.VERTICAL,
                    'suspicion_level': admin.VERTICAL,
                    'performance': admin.VERTICAL,
                    'pain_score': admin.VERTICAL,
                    'last_hiv_result': admin.VERTICAL,
                    'patient_disposition': admin.VERTICAL,
                    'referral_unit': admin.VERTICAL,
                    'referral_discussed': admin.VERTICAL,
                    'referral_fu': admin.VERTICAL,
                    'triage_status': admin.VERTICAL,
                    'investigated': admin.VERTICAL,
                    'vehicle_req': admin.VERTICAL,
                    'paper_register': admin.VERTICAL,
                    }

    readonly_fields = ('screening_identifier',)

    filter_horizontal = ('symptoms', )

    actions = ['export_crf_as_csv']

    search_fields = ('screening_identifier',)

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) + audit_fields)
