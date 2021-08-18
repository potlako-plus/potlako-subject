from django import forms
from edc_constants.constants import DONE

from ..models import NavigationSummaryAndPlan, EvaluationTimeline


class NavigationSummaryAndPlanForm(forms.ModelForm):

    class Meta:
        model = NavigationSummaryAndPlan
        fields = '__all__'


class EvaluationTimelineForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        completion_date = cleaned_data.get('completion_date')
        step_status = cleaned_data.get('key_step_status')

        if completion_date and step_status != DONE:
            raise forms.ValidationError({
                'key_step_status':
                'Please set status done if key step achieved.'})
        if step_status == DONE and not completion_date:
            raise forms.ValidationError({
                'completion_date':
                'Please specify achieved date if key step is done.'})

    class Meta:
        model = EvaluationTimeline
        fields = '__all__'
