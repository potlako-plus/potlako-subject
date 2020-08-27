from django import forms

from ..models import BaselineClinicalSummary
from .form_mixins import SubjectModelFormMixin


class BaselineClinicalSummaryForm(SubjectModelFormMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = BaselineClinicalSummary
        fields = '__all__'
