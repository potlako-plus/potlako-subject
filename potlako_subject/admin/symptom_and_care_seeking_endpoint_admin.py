from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import SymptomAndcareSeekingEndpointForm
from ..models import SymptomsAndCareSeekingEndpointRecording

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SymptomsAndCareSeekingEndpointRecording, site=potlako_subject_admin)
class SymptomAndcareSeekingEndpointAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SymptomAndcareSeekingEndpointForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'cancer_symptom_date',
                       'cancer_symptom_estimated',
                       'cancer_symptom_estimation',
                       'discussion_date',
                       'discussion_date_estimated',
                       'discussion_date_estimation',
                       'seek_help_date',
                       'seek_help_date_estimated',
                       'seek_help_date_estimation',
                       'first_seen_date',
                       'first_seen_date_estimated',
                       'first_seen_date_estimation'),
        }),
    )

    radio_fields = {'cancer_symptom_estimated': admin.VERTICAL,
                    'cancer_symptom_estimation': admin.VERTICAL,
                    'discussion_date_estimated': admin.VERTICAL,
                    'discussion_date_estimation': admin.VERTICAL,
                    'seek_help_date_estimated': admin.VERTICAL,
                    'seek_help_date_estimation': admin.VERTICAL,
                    'first_seen_date_estimated': admin.VERTICAL,
                    'first_seen_date_estimation': admin.VERTICAL,
                    }
