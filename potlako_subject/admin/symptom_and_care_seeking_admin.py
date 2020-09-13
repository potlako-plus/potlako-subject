from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import potlako_subject_admin
from ..forms import SymptomAndcareSeekingAssessmentForm, SymptomAssessmentForm
from ..models import SymptomAndcareSeekingAssessment, SymptomAssessment
from .modeladmin_mixins import CrfModelAdminMixin


class EvaluationTimelineInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = SymptomAssessment
    form = SymptomAssessmentForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': [
                'symptom',
                'symptom_date',
                'last_visit_date_estimated',
                'last_visit_date_estimation']}
         ),)


@admin.register(SymptomAndcareSeekingAssessment, site=potlako_subject_admin)
class SymptomAndcareSeekingAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SymptomAndcareSeekingAssessmentForm
    inlines = [EvaluationTimelineInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'first_visit_promt',
                       'symptoms_cope',
                       'symptoms_present',
                       'symptoms_present_other',
                       'symptoms_discussion',
                       'reason_no_discussion',
                       'reason_no_discussion_other',
                       'discussion_person',
                       'discussion_person_other',
                       'discussion_date',
                       'discussion_date_estimated',
                       'discussion_date_estimation',
                       'medical_advice',
                       'clinic_visit_date',
                       'clinic_visit_date_estimated',
                       'clinic_visit_date_estimation',
                       'clinic_visited',
                       'clinic_visited_other',
                       'cause_assumption',
                       'symptoms_concern'),
        }), audit_fieldset_tuple
    )

    radio_fields = {'symptoms_discussion': admin.VERTICAL,
                    'reason_no_discussion': admin.VERTICAL,
                    'discussion_date_estimated': admin.VERTICAL,
                    'discussion_date_estimation': admin.VERTICAL,
                    'medical_advice': admin.VERTICAL,
                    'clinic_visit_date_estimated': admin.VERTICAL,
                    'clinic_visit_date_estimation': admin.VERTICAL,
                    'symptoms_concern': admin.VERTICAL,
                    }

    filter_horizontal = ('symptoms_present', 'discussion_person', )
