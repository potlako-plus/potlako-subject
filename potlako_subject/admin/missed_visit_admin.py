from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import MissedVisitForm
from ..models import MissedVisit


@admin.register(MissedVisit, site=potlako_subject_admin)
class MissedVisitAdmin(admin.ModelAdmin):

    form = MissedVisitForm

    fieldsets = (
        (None, {
            'fields': ('report_datetime',
                       'missed_visit_date',
                       'facility_scheduled',
                       'visit_type',
                       'determine_missed',
                       'inquired',
                       'inquired_from',
                       'reason_missed',
                       'reason_other',
                       'next_appointment',
                       'next_ap_facility',
                       'next_ap_type',
                       'home_visit',
                       'transport_need',
                       'clinician_name',
                       'comments'),
        }),
    )

    radio_fields = {'facility_scheduled': admin.VERTICAL,
                    'visit_type': admin.VERTICAL,
                    'determine_missed': admin.VERTICAL,
                    'inquired': admin.VERTICAL,
                    'inquired_from': admin.VERTICAL,
                    'reason_missed': admin.VERTICAL,
                    'next_ap_facility': admin.VERTICAL,
                    'next_ap_type': admin.VERTICAL,
                    'home_visit': admin.VERTICAL,
                    'transport_need': admin.VERTICAL}
