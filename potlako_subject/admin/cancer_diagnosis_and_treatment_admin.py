from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import CancerDiagnosisAndTreatmentAssessmentForm
from ..models import CancerDiagnosisAndTreatmentAssessment

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CancerDiagnosisAndTreatmentAssessment, site=potlako_subject_admin)
class CancerDiagnosisAndTreatmentAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CancerDiagnosisAndTreatmentAssessmentForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'symptoms_summary',
                       'cancer_evaluation',
                       'diagnosis_date',
                       'diagnosis_date_estimated',
                       'diagnosis_date_estimation',
                       'clinical_impression',
                       'cancer_treatment',
                       'treatment_description'),
        }),
    )

    radio_fields = {
        'cancer_evaluation': admin.VERTICAL,
        'diagnosis_date_estimated': admin.VERTICAL,
        'diagnosis_date_estimation': admin.VERTICAL,
        'cancer_treatment': admin.VERTICAL,
    }
