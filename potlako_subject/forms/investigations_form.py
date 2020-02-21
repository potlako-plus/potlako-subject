from django import forms

from ..models import Investigations, LabTest
from .form_mixins import SubjectModelFormMixin


class InvestigationsForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = Investigations
        fields = '__all__'


class LabTestForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = LabTest
        fields = '__all__'
