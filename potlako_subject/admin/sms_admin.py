from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import SMSForm
from ..models import SMS


@admin.register(SMS, site=potlako_subject_admin)
class SMSAdmin(admin.ModelAdmin):

    form = SMSForm

    fieldsets = (
        (None, {
            'fields': ('date_time_form_filled',
                       'next_ap_date',
                       'date_reminder_sent',
                       'sms_outcome'),
            }),
    )

    radio_fields = {'sms_outcome': admin.VERTICAL}
