from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import BaselineRoadMapForm
from ..models import BaselineRoadMap

from .modeladmin_mixins import ModelAdminMixin


@admin.register(BaselineRoadMap, site=potlako_subject_admin)
class BaselineRoadMapAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = BaselineRoadMapForm

    fieldsets = (
        (None, {
            'fields': ('report_datetime',
                       'investigations_turnaround_time',
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
        }),
    )

    radio_fields = {
        'specialty_clinic': admin.VERTICAL,
        'specialist_clinic_type': admin.VERTICAL,
        'results_review_personnel': admin.VERTICAL
    }
