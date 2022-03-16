from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple, ModelAdminReadOnlyMixin
from ..admin_site import potlako_subject_admin
from ..forms import NavigationSummaryAndPlanForm, EvaluationTimelineForm
from ..models import NavigationSummaryAndPlan, EvaluationTimeline
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
                'adjusted_target_date',
                'key_step_status',
                'completion_date',
                'review_required')}
         ),)

    def has_change_permission(self, request, obj):
        return not request.GET.get('edc_readonly')

    def has_add_permission(self, request, obj):
        return not request.GET.get('edc_readonly')


@admin.register(NavigationSummaryAndPlan, site=potlako_subject_admin)
class NavigationPlanAndSummaryAdmin(ModelAdminMixin, ModelAdminReadOnlyMixin, admin.ModelAdmin):

    form = NavigationSummaryAndPlanForm
    inlines = [EvaluationTimelineInlineAdmin, ]
    instructions = None
    extra_context_models = ['cliniciancallenrollment',
                            'baselineclinicalsummary',
                            'symptomandcareseekingassessment',
                            'cancerdxandtx', ]

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'diagnostic_plan',
                'notes']}
         ), audit_fieldset_tuple)

    search_fields = ('subject_identifier',)
