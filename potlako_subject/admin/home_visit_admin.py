from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import HomeVisitForm
from ..models import HomeVisit

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HomeVisit, site=potlako_subject_admin)
class HomeVisitAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HomeVisitForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'clinician_type',
                       'clinician_type_other',
                       'clinician_facility',
                       'clinician_facility_other',
                       'visit_outcome',
                       'visit_outcome_other',
                       'next_appointment',
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'next_ap_type',
                       'general_comments'),
        }),
    )

    radio_fields = {
        'clinician_type': admin.VERTICAL,
        'clinician_facility': admin.VERTICAL,
        'visit_outcome': admin.VERTICAL,
        'next_ap_facility': admin.VERTICAL,
        'next_ap_type': admin.VERTICAL,
    }
