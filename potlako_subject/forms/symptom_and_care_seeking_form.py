from django import forms
from ..models import SymptomAndcareSeekingAssessment, SymptomAssessment
from .form_mixins import SubjectModelFormMixin


class SymptomAndcareSeekingAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = SymptomAndcareSeekingAssessment
        fields = '__all__'


class SymptomAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = SymptomAssessment
        fields = '__all__'
