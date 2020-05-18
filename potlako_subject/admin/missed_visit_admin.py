from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import MissedVisitForm
from ..models import MissedVisit

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(MissedVisit, site=potlako_subject_admin)
class MissedVisitAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MissedVisitForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'missed_visit_date',
                       'inquired',
                       'not_inquired_reason',
                       'not_inquired_reason_other',
                       'facility_scheduled',
                       'facility_scheduled_other',
                       'visit_type',
                       'determine_missed',
                       'determine_missed_other',
                       'inquired_from',
                       'reason_missed',
                       'reason_other',
                       'next_appointment',
                       'next_ap_facility',
                       'next_ap_facility_other',
                       'next_ap_type',
                       'home_visit',
                       'transport_need',
                       'transport_support',
                       'clinician_designation',
                       'clinician_designation_other',
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
                    'transport_need': admin.VERTICAL,
                    'transport_support': admin.VERTICAL,
                    'clinician_designation': admin.VERTICAL, }
