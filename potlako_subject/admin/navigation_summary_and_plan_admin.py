from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import NavigationSummaryAndPlanForm, EvaluationTimelineForm
from ..models import NavigationSummaryAndPlan, EvaluationTimeline
from .modeladmin_mixins import ModelAdminMixin
from ..models.model_mixins import BaselineRoadMapMixin

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


@admin.register(NavigationSummaryAndPlan, site=potlako_subject_admin)
class NavigationPlanAndSummaryAdmin(ModelAdminMixin, admin.ModelAdmin):


    form = NavigationSummaryAndPlanForm
    inlines = [EvaluationTimelineInlineAdmin, ]
    instructions = None

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'diagnostic_plan', ]}
         ), audit_fieldset_tuple)
    
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = BaselineRoadMapMixin(subject_identifier=request.GET.get(
            'subject_identifier')).baseline_dict
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = BaselineRoadMapMixin(subject_identifier=request.GET.get(
            'subject_identifier')).baseline_dict
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
        