from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
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
                       'notes',
                       'repeat_call'),
        }), audit_fieldset_tuple)

    list_display = ('repeat_call',)
