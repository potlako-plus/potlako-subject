from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import PatientCallFollowUp


class PatientCallFollowUpForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    # form_validator_cls = ClinicianCallEnrollmentFormValidator

    class Meta:
        model = PatientCallFollowUp
        fields = '__all__'
