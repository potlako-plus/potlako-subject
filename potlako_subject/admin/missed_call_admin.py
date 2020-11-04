from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin
from ..admin_site import potlako_subject_admin
from ..forms import MissedCallForm, MissedCallRecordForm
from ..models import MissedCall, MissedCallRecord

from .modeladmin_mixins import CrfModelAdminMixin


class MissedCallRecordInlineAdmin(TabularInlineMixin, admin.TabularInline):
    
    model = MissedCallRecord
    form = MissedCallRecordForm
    extra = 2
    max_num = 3

    fieldsets = (
        (None, {
            'fields': ('notes',
                       'repeat_call'),
        }), audit_fieldset_tuple)

    list_display = ('repeat_call',)
    
    
@admin.register(MissedCall, site=potlako_subject_admin)
class MissedCallAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MissedCallForm
    
    inlines = [MissedCallRecordInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',)
        }), audit_fieldset_tuple)

