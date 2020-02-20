from django import forms

from ..models import ClinicianCallFollowUp
from .form_mixins import SubjectModelFormMixin


class ClinicianCallFollowUpForm(SubjectModelFormMixin, forms.ModelForm):

    # form_validator_cls = ClinicianCallEnrollmentFormValidator

    class Meta:
        model = ClinicianCallFollowUp
        fields = '__all__'
