from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import SymptomAndcareSeekingAssessmentForm
from ..models import SymptomAndcareSeekingAssessment

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SymptomAndcareSeekingAssessment, site=potlako_subject_admin)
class SymptomAndcareSeekingAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SymptomAndcareSeekingAssessmentForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'first_visit_promt',
                       'symptoms_description',
                       'symptoms_present',
                       'symptoms_discussion',
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
                       'cause_assumption',
                       'symptoms_concern'),
        }),
    )

    radio_fields = {'symptoms_discussion': admin.VERTICAL,
                    'discussion_person': admin.VERTICAL,
                    'discussion_date_estimated': admin.VERTICAL,
                    'discussion_date_estimation': admin.VERTICAL,
                    'medical_advice': admin.VERTICAL,
                    'clinic_visit_date_estimated': admin.VERTICAL,
                    'clinic_visit_date_estimation': admin.VERTICAL,
                    'clinic_visited': admin.VERTICAL,
                    'symptoms_concern': admin.VERTICAL,
                    }

    filter_horizontal = ('symptoms_present',)
