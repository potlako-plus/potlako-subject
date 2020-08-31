from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple
from django.http import HttpRequest, request
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

#     print("????????????????",request.QueryDict)
#     patient_details_dict =  BaselineRoadMapMixin(
#         request.GET['subject_visit'].subject_identifier,
#         request.GET['subject_visit'])
#     s = patient_details_dict.get('hiv_status')
    

    form = NavigationSummaryAndPlanForm
    inlines = [EvaluationTimelineInlineAdmin, ]
#     patient_summary = patient_details
    instructions = None

    fieldsets = (
        (None, {
            'fields': [
                'diagnostic_plan', ]}
         ), audit_fieldset_tuple)
    
#     def get_patient_summary(self, request, extra_context):
#         import pdb; pdb.set_trace()
#         
#         extra_context = extra_context or {}
#         extra_context[
#             'patient_summary'] = self.patient_details
#         return extra_context    
#     
#     def add_view(self, request, form_url='', extra_context=None):
#         extra_context = self.get_patient_summary(request, extra_context)
#         return super().add_view(
#             request, form_url=form_url, extra_context=extra_context)
# 
#     def change_view(self, request, object_id, form_url='', extra_context=None):
#         extra_context = self.get_patient_summary(request, extra_context)
#         return super().change_view(
#             request, object_id, form_url=form_url, extra_context=extra_context)
#         
#     def get_changeform_initial_data(self, request):
#         return {'patient_details': 'custom_initial_value'}
#     
#     @property
#     def patient_details(self):
#         import pdb; pdb.set_trace()
#         patient_details_dict =  BaselineRoadMapMixin(HttpRequest.GET.dict().get('subject_visit').subject_identifier,
#                                     HttpRequest.GET.dict().get('subject_visit'))
#         return [patient_details_dict.get('hiv_status')]
