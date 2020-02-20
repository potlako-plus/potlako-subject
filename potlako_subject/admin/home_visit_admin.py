from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from ..admin_site import potlako_subject_admin
from ..forms import HomeVisitForm
from ..models import HomeVisit


@admin.register(HomeVisit, site=potlako_subject_admin)
class HomeVisitAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    form = HomeVisitForm

    fieldsets = (
        (None, {
            'fields': ('visit_date_time',
                       'clinician_name',
                       'clinician_type',
                       'facility_clinician_works',
                       'clinician_two_name',
                       'clinician_two_type',
                       'clinician_two_facility',
                       'clinician_three_name',
                       'clinician_three_type',
                       'clinician_three_facility',
                       'visit_outcome',
                       'next_appointment',
                       'next_ap_facility',
                       'nex_ap_type',
                       'general_comments'),
        }),
    )

    radio_fields = {
        'clinician_type': admin.VERTICAL,
        'facility_clinician_works': admin.VERTICAL,
        'clinician_two_type': admin.VERTICAL,
        'clinician_two_facility': admin.VERTICAL,
        'clinician_three_type': admin.VERTICAL,
        'clinician_three_facility': admin.VERTICAL,
        'visit_outcome': admin.VERTICAL,
        'next_ap_facility': admin.VERTICAL,
        'nex_ap_type': admin.VERTICAL,
    }
