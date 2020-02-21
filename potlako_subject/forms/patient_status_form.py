from django import forms

from ..models import PatientStatus
from .form_mixins import SubjectModelFormMixin


class PatientStatusForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = PatientStatus
        fields = '__all__'
