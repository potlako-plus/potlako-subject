from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import potlako_subject_admin
from ..forms import NavigationPlanAndSummaryForm, EvaluationTimelineForm
from ..models import NavigationPlanAndSummary, EvaluationTimeline
from .modeladmin_mixins import ModelAdminMixin


class EvaluationTimelineInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = EvaluationTimeline
    form = EvaluationTimelineForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'key_step',
                'target_date',
                'key_step_status',
                'completion_date',
                'review_required')}
         ),)


@admin.register(NavigationPlanAndSummary, site=potlako_subject_admin)
class NavigationPlanAndSummaryAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = NavigationPlanAndSummaryForm
    inlines = [EvaluationTimelineInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'diagnostic_plan', ]}
         ), audit_fieldset_tuple)
