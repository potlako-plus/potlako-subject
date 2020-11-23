from django.contrib import admin
from edc_base.utils import get_utcnow
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin
from dateutil.relativedelta import relativedelta
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


class RepeatCallFilter(admin.SimpleListFilter):
    title = 'Repeat call date'
    parameter_name = 'repeat_calls'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Today'),
            ('weekly', 'This week'),
            ('monthly', 'This month')]

    def queryset(self, request, queryset):
        if self.value() == 'today':
            missedcallrecord_qs = MissedCallRecord.objects.filter(
                repeat_call=get_utcnow().date())
            return self.related_qs(queryset, missedcallrecord_qs)
        if self.value() == 'weekly':
            one_week = get_utcnow() + relativedelta(days=7)
            missedcallrecord_qs = MissedCallRecord.objects.filter(
                repeat_call__range=[get_utcnow().date(), one_week.date()])
            return self.related_qs(queryset, missedcallrecord_qs)
        if self.value() == 'monthly':
            missedcallrecord_qs = MissedCallRecord.objects.filter(
                repeat_call__month=get_utcnow().month)
            return self.related_qs(queryset, missedcallrecord_qs)

    def related_qs(self, queryset, qs):
        return queryset.filter(id__in=qs.values('missed_call_id'))


@admin.register(MissedCall, site=potlako_subject_admin)
class MissedCallAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MissedCallForm

    inlines = [MissedCallRecordInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': ('subject_visit',)
        }), audit_fieldset_tuple)

    list_filter = (RepeatCallFilter, )
