from django import forms

from ..models import PatientCallFollowUp
from .form_mixins import SubjectModelFormMixin


class PatientCallFollowUpForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = PatientCallFollowUp
        fields = '__all__'
