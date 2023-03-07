from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import CancerDxAndTxAssessmentForm
from ..models import CancerDxAndTx
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CancerDxAndTx, site=potlako_subject_admin)
class CancerDxAndTxAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CancerDxAndTxAssessmentForm
    extra_context_models = ['cliniciancallenrollment',
                            'baselineclinicalsummary',
                            'patientcallinitial',
                            'navigationplanandsummary',
                            'extra_symptoms_description']

    list_filter = ['cancer_treatment']

    search_fields = ('subject_visit', 'cancer_evaluation', 'cancer_treatment')

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'symptoms_summary',
                       'cancer_evaluation',
                       'diagnosis_date',
                       'diagnosis_date_estimated',
                       'diagnosis_date_estimation',
                       'cancer_treatment',
                       'treatment_description'),
        }), audit_fieldset_tuple)

    radio_fields = {
        'cancer_evaluation': admin.VERTICAL,
        'diagnosis_date_estimated': admin.VERTICAL,
        'diagnosis_date_estimation': admin.VERTICAL,
        'cancer_treatment': admin.VERTICAL,
    }

    list_display = ('subject_visit', 'cancer_evaluation', 'cancer_treatment')
