from django import forms

from ..models import PatientCallInitial
from .form_mixins import SubjectModelFormMixin


class PatientCallInitialForm(SubjectModelFormMixin, forms.ModelForm):

    # form_validator_cls = ClinicianCallEnrollmentFormValidator

    class Meta:
        model = PatientCallInitial
        fields = '__all__'
