from django import forms
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from potlako_validations.form_validators import ClinicianCallEnrollmentFormValidator

from ..models import ClinicianCallEnrollment


class ClinicianCallEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ClinicianCallEnrollmentFormValidator
    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        date_registered = self.cleaned_data.get('reg_date')
        report_datetime = self.cleaned_data.get('report_datetime')

        if date_registered > report_datetime.date():
            raise ValidationError('Date patient was registered at facility'
                                  ' should be earlier than report datetime.')
        super().clean()

    class Meta:
        model = ClinicianCallEnrollment
        fields = '__all__'
