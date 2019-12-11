from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import PatientStatusForm
from ..models import PatientStatus


@admin.register(PatientStatus, site=potlako_subject_admin)
class PatientStatusAdmin(admin.ModelAdmin):

    form = PatientStatusForm

    fieldsets = (
        (None, {
            'fields': ('last_encounter',
                       'sms_due',
                       'days_from_recent_visit',
                       'physician_flag',
                       'bpcc_bid_entered',
                       'bcpp_enrolled',
                       'deceased',
                       'days_from_death_report',
                       'calc_hiv_status',
                       'missed_calls',
                       'seen_at_marina',
                       'exit_status',
                       'first_last_visit_days',
                       'missed_visits',),
        }),
    )
