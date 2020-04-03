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
                       'clinician_name',
                       'clinician_type',
                       'clinician_facility',
                       'clinician_facility_other',
                       'clinician_two_name',
                       'clinician_two_type',
                       'clinician_two_facility',
                       'clinician_two_facility_other',
                       'clinician_three_name',
                       'clinician_three_type',
                       'clinician_three_facility',
                       'clinician_three_facility_other,'
                       'visit_outcome',
                       'next_appointment',
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'nex_ap_type',
                       'general_comments'),
        }),
    )

    radio_fields = {
        'clinician_type': admin.VERTICAL,
        'clinician_facility': admin.VERTICAL,
        'clinician_two_type': admin.VERTICAL,
        'clinician_two_facility': admin.VERTICAL,
        'clinician_three_type': admin.VERTICAL,
        'clinician_three_facility': admin.VERTICAL,
        'visit_outcome': admin.VERTICAL,
        'next_ap_facility': admin.VERTICAL,
        'nex_ap_type': admin.VERTICAL,
    }
