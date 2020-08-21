from django import forms
from ..models import NavigationPlanAndSummary, EvaluationTimeline


class NavigationPlanAndSummaryForm(forms.ModelForm):

    class Meta:
        model = NavigationPlanAndSummary
        fields = '__all__'


class EvaluationTimelineForm(forms.ModelForm):

    class Meta:
        model = EvaluationTimeline
        fields = '__all__'
