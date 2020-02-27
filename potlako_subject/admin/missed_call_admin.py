from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import MissedCallForm
from ..models import MissedCall

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(MissedCall, site=potlako_subject_admin)
class MissedCallAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MissedCallForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'report_datetime',
                       'entry_date',
                       'notes',
                       'repeat_call'),
        }),
    )

    list_display = ('entry_date', 'repeat_call')
