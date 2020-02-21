from django.contrib import admin
from ..admin_site import potlako_subject_admin
from ..forms import SMSForm
from ..models import SMS

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SMS, site=potlako_subject_admin)
class SMSAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SMSForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'date_time_form_filled',
                       'next_ap_date',
                       'date_reminder_sent',
                       'sms_outcome'),
        }),
    )

    radio_fields = {'sms_outcome': admin.VERTICAL}

    list_display = ('date_time_form_filled', 'next_ap_date',
                    'date_reminder_sent', 'sms_outcome')
