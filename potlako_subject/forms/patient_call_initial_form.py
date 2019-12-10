from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import PatientCallInitial


class PatientCallInitialForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    # form_validator_cls = ClinicianCallEnrollmentFormValidator

    class Meta:
        model = PatientCallInitial
        fields = '__all__'
