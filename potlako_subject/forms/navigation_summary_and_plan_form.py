from django import forms
from ..models import NavigationSummaryAndPlan, EvaluationTimeline


class NavigationSummaryAndPlanForm(forms.ModelForm):

    class Meta:
        model = NavigationSummaryAndPlan
        fields = '__all__'


class EvaluationTimelineForm(forms.ModelForm):

    class Meta:
        model = EvaluationTimeline
        fields = '__all__'
