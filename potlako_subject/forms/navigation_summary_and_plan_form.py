from datetime import datetime
from django.conf import settings
from django import forms
from edc_base.utils import get_utcnow
from ..models import NavigationSummaryAndPlan, EvaluationTimeline


class NavigationSummaryAndPlanForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        evaluation_count = self.data.get(
            'evaluationtimeline_set-TOTAL_FORMS')

        for count in range(int(evaluation_count)):

            target_date = self.data.get(
                'evaluationtimeline_set-' + str(count) + '-target_date')

            completion_date = self.data.get(
                'evaluationtimeline_set-' + str(count) + '-completion_date')
            if target_date:
                target_date = datetime.strptime(target_date, settings.DATE_INPUT_FORMATS[0]).date()
                if not self.data.get('evaluationtimeline_set-' + str(count) + '-id'):
                    if target_date < get_utcnow().date():
                        raise forms.ValidationError(
                        'Target date for evaluation timeline  entry number '
                         ' must be a future date from now. Check entry number ' + str(count + 1))

                if completion_date:
                    completion_date = datetime.strptime(completion_date, settings.DATE_INPUT_FORMATS[0]).date()
                    if completion_date < target_date:
                        raise forms.ValidationError(
                            'Completion date cannot be before target date.'
                            'Check entry number ' + str(count + 1))


    class Meta:
        model = NavigationSummaryAndPlan
        fields = '__all__'


class EvaluationTimelineForm(forms.ModelForm):



    class Meta:
        model = EvaluationTimeline
        fields = '__all__'
