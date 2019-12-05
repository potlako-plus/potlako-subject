from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import ClinicianCallEnrollmentForm
from ..models import ClinicianCallEnrollment


@admin.register(ClinicianCallEnrollment, site=potlako_subject_admin)
class ClinicianCallEnrollmentAdmin(admin.ModelAdmin):

    form = ClinicianCallEnrollmentForm

    fieldsets = (
        (None, {
            'fields': ('reg_date',
                       'record_id',
                       'call_start',
                       'contact_date',
                       'call_clinician',
                       'call_clinician_type',
                       'call_clinician_other',
                       'received_training',
                       'facility',
                       'facility_unit',
                       'unit_other',
                       'national_identity',
                       'hospital_identity',
                       'same_clinician',
                       'more_clinicians',
                       'clinician_name',
                       'clinician_type',
                       'symptoms',
                       'early_symptoms_date',
                       'patient_disposition',
                       )
        }),
        ('Personal Details', {
            'fields': ('last_name',
                       'first_name',
                       'dob',
                       'age_in_years',
                       'gender',
                       'residence',
                       'village_town',
                       'kgotla',
                       'nearest_facility',
                       'near_facility_other',
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
    )

    radio_fields = {'call_clinician_type': admin.VERTICAL,
                    'received_training': admin.VERTICAL,
                    'facility': admin.VERTICAL,
                    'facility_unit': admin.VERTICAL,
                    'gender': admin.VERTICAL,
                    'residence': admin.VERTICAL,
                    'nearest_facility': admin.VERTICAL,
                    'kin_relationship': admin.VERTICAL,
                    'other_kin_avail': admin.VERTICAL,
                    'other_kin_rel': admin.VERTICAL,
                    'same_clinician': admin.VERTICAL,
                    'more_clinicians': admin.VERTICAL,
                    'clinician_type': admin.VERTICAL,
                    }

    filter_horizontal = ('patient_disposition', )
