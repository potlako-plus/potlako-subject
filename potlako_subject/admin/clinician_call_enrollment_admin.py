from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import potlako_subject_admin
from ..forms import ClinicianCallEnrollmentForm, NextOfKinForm
from ..models import ClinicianCallEnrollment, NextOfKin
from .subject_screening_admin import ModelAdminMixin


class NextOfKinInlineAdmin(TabularInlineMixin, admin.TabularInline):

    model = NextOfKin
    form = NextOfKinForm
    extra = 1
    max_num = 2

    fieldsets = (
        (None, {
            'fields': (
                'kin_lastname',
                'kin_firstname',
                'kin_relationship',
                'kin_relation_other',
                'kin_cell',
                'kin_telephone')}
         ),)


@admin.register(ClinicianCallEnrollment, site=potlako_subject_admin)
class ClinicianCallEnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicianCallEnrollmentForm
    inlines = [NextOfKinInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('report_datetime',
                       'reg_date',
                       'screening_identifier',
                       'cancer_suspect',
                       'cancer_suspect_other',
                       'call_clinician_type',
                       'call_clinician_other',
                       'consented_contact',
                       'paper_register',
                       'received_training',
                       'facility',
                       'facility_other',
                       'facility_unit',
                       'unit_other',)
        }),
        ('Personal Details', {
            'fields': (
                'last_name',
                'first_name',
                'age_in_years',
                'gender',
                'national_identity',
                'hospital_identity',
                'village_town',
                'patient_contact',
                'primary_cell',
                'secondary_cell',
                'telephone_number',
                'kin_details_provided',
            )
        }),
        ('Symptoms Details', {
            'fields': (
                'clinician_type',
                'clinician_other',
                'symptoms',
                'symptoms_other',
                'early_symptoms_date',
                'early_symptoms_date_estimated',
                'early_symptoms_date_estimation',
                'suspected_cancer',
                'suspected_cancer_unsure',
                'suspected_cancer_other',
                'suspicion_level',
                'performance',
                'pain_score',
                'last_hiv_result',
                'patient_disposition',)
        }),
        ('Referral Details', {
            'fields': (
                'referral_reason',
                'referral_facility',
                'referral_facility_other',
                'referral_unit',
                'referral_unit_other',
                'referral_discussed',
                'referral_date',)
        }),
        ('Extra Details', {
            'fields': (
                'triage_status',
                'investigated',
                'tests_ordered',
                'comments',)
        }),

        audit_fieldset_tuple
    )

    radio_fields = {'cancer_suspect': admin.VERTICAL,
                    'call_clinician_type': admin.VERTICAL,
                    'consented_contact': admin.VERTICAL,
                    'received_training': admin.VERTICAL,
                    'facility_unit': admin.VERTICAL,
                    'gender': admin.VERTICAL,
                    'patient_contact': admin.VERTICAL,
                    'kin_details_provided': admin.VERTICAL,
                    'clinician_type': admin.VERTICAL,
                    'early_symptoms_date_estimated': admin.VERTICAL,
                    'early_symptoms_date_estimation': admin.VERTICAL,
                    'suspected_cancer': admin.VERTICAL,
                    'suspicion_level': admin.VERTICAL,
                    'performance': admin.VERTICAL,
                    'pain_score': admin.VERTICAL,
                    'last_hiv_result': admin.VERTICAL,
                    'patient_disposition': admin.VERTICAL,
                    'referral_unit': admin.VERTICAL,
                    'referral_discussed': admin.VERTICAL,
                    'triage_status': admin.VERTICAL,
                    'investigated': admin.VERTICAL,
                    'paper_register': admin.VERTICAL,
                    }

    readonly_fields = ('screening_identifier',)

    filter_horizontal = ('symptoms',)

    actions = ['export_crf_as_csv']

    search_fields = ('screening_identifier',)
