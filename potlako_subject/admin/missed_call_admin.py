from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import MissedCallForm
from ..models import MissedCall


@admin.register(MissedCall, site=potlako_subject_admin)
class MissedCallAdmin(admin.ModelAdmin):

    form = MissedCallForm

    fieldsets = (
        (None, {
            'fields': ('entry_date',
                       'notes',
                       'repeat_call'),
        }),
    )

    list_display = ('entry_date', 'repeat_call')
