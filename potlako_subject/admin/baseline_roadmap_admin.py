from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import potlako_subject_admin
from ..constants import UNSURE
from ..forms import BaselineRoadMapForm
from ..models import BaselineRoadMap, ClinicianCallEnrollment
from .modeladmin_mixins import ModelAdminMixin


@admin.register(BaselineRoadMap, site=potlako_subject_admin)
class BaselineRoadMapAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = BaselineRoadMapForm

    fieldsets = (
        (None, {
            'fields': ('investigations_turnaround_time',
                       'specialty_clinic',
                       'specialist_clinic_type',
                       'specialist_clinic_type_other',
                       'specialist_turnaround_time',
                       'results_review_personnel',
                       'results_review_personnel_other',
                       'review_turnaround_time',
                       'oncology_visit',
                       'oncology_turnaround_time',
                       'treatment_initiation_visit',
                       'treatment_initiation_turnaround_time'),
        }), audit_fieldset_tuple)

    radio_fields = {
        'specialty_clinic': admin.VERTICAL,
        'specialist_clinic_type': admin.VERTICAL,
        'results_review_personnel': admin.VERTICAL
    }

    list_display = ('subject_identifier',
                    'specialist_turnaround_time',
                    'review_turnaround_time',
                    'oncology_visit',
                    'oncology_turnaround_time',
                    'treatment_initiation_visit')

    def get_clinician_call_attrs(self, subject_identifier=None):
        """Extract values required for Baseline Map from Clinician Call
        Enrollment model.
        """

        enrollment_dict = {}
        attributes = ['suspected_cancer', 'suspected_cancer_other',
                      'gender', 'suspicion_level']

        try:
            clinician_call_obj = ClinicianCallEnrollment.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            for attr in attributes:
                value = getattr(
                    clinician_call_obj, 'suspected_cancer')

                if attr == 'suspected_cancer' and value == UNSURE:
                    value = getattr(
                        clinician_call_obj, 'suspected_cancer_unsure')

                enrollment_dict.update({attr: value})

        return enrollment_dict
