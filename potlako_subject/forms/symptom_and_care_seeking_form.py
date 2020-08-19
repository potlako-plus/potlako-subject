from django import forms
from ..models import SymptomAndcareSeekingAssessment
from .form_mixins import SubjectModelFormMixin


class SymptomAndcareSeekingAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = SymptomAndcareSeekingAssessment
        fields = '__all__'
