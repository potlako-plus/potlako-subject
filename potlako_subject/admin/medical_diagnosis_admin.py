from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import MedicalConditionsForm, MedicalDiagnosisForm
from ..models import MedicalConditions, MedicalDiagnosis
from .modeladmin_mixins import CrfModelAdminMixin


class MedicalConditionsInlineAdmin(TabularInlineMixin, admin.TabularInline):

    model = MedicalConditions
    form = MedicalConditionsForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'medical_condition',
                'medical_condition_other',
                'medical_condition_specify',
                'diagnosis_date',
                'diagnosis_date_estimate',
                'diagnosis_date_estimation',
                'on_medication',
                'treatment_type',
                'treatment_name')}
         ),)


@admin.register(MedicalDiagnosis, site=potlako_subject_admin)
class MedicalDiagnosisAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MedicalDiagnosisForm

    inlines = [MedicalConditionsInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',)
        }), audit_fieldset_tuple)
