from django import forms

from ..models import BaselineClinicalSummary
from .form_mixins import SubjectModelFormMixin


class BaselineClinicalSummaryForm(SubjectModelFormMixin, forms.ModelForm):

    pass

    class Meta:
        model = BaselineClinicalSummary
        fields = '__all__'
