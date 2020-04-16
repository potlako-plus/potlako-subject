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
                       'info_from_clinician',
                       'info_source_specify',
                       'call_clinician_type',
                       'call_clinician_other',
                       'consented_contact',
                       'paper_register',
                       'received_training',
                       'facility',
                       'facility_other',
                       'facility_unit',
                       'unit_other',
                       'clinician_type',
                       'clinician_other',
                       'symptoms',
                       'symptoms_other',
                       'early_symptoms_date',
                       'early_symptoms_date_estimated',
                       'early_symptoms_date_estimation',
                       'symptoms_details',
                       'suspected_cancer',
                       'suspected_cancer_other',
                       'suspicion_level',
                       'performance',
                       'pain_score',
                       'last_hiv_result',
                       'patient_disposition',
                       'referral_reason',
                       'referral_date',
                       'referral_facility',
                       'referral_facility_other',
                       'referral_unit',
                       'referral_discussed',
                       'clinician_designation',
                       'referral_fu_date',
                       'triage_status',
                       'investigated',
                       'notes',
                       'comments',
                       )
        }),
        ('Personal Details', {
            'fields': (
                'national_identity',
                'hospital_identity',
                'last_name',
                'first_name',
                'age_in_years',
                'gender',
                'village_town',
                'kgotla',
                'nearest_facility',
                'nearest_facility_other',
                'primary_cell',
                'secondary_cell',
                'kin_firstname',
                'kin_lastname',
                'kin_relationship',
                'kin_relation_other',
                'kin_cell',
                'other_kin_avail',
                'other_kin_lastname',
                'other_kin_firstname',
                'other_kin_rel',
                'other_kin_rel_other',
                'other_kin_cell',
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
                    'early_symptoms_date_estimated': admin.VERTICAL,
                    'suspected_cancer': admin.VERTICAL,
                    'suspicion_level': admin.VERTICAL,
                    'performance': admin.VERTICAL,
                    'pain_score': admin.VERTICAL,
                    'last_hiv_result': admin.VERTICAL,
                    'patient_disposition': admin.VERTICAL,
                    'referral_facility': admin.VERTICAL,
                    'referral_unit': admin.VERTICAL,
                    'referral_discussed': admin.VERTICAL,
                    'triage_status': admin.VERTICAL,
                    'investigated': admin.VERTICAL,
                    'paper_register': admin.VERTICAL,
                    'notes': admin.VERTICAL,
                    }

    readonly_fields = ('screening_identifier',)

    filter_horizontal = ('symptoms',)

    actions = ['export_crf_as_csv']

    search_fields = ('screening_identifier',)

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj) + ('age_in_years',) + audit_fields)
