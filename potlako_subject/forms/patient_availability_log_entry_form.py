from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import PatientAvailabilityLog, PatientAvailabilityLogEntry
from potlako_validations.form_validators import PatientAvailabilityLogEntryFormValidator


class PatientAvailabilityLogForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = PatientAvailabilityLog
        fields = '__all__'


class PatientAvailabilityLogEntryForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = PatientAvailabilityLogEntryFormValidator

    class Meta:
        model = PatientAvailabilityLogEntry
        fields = '__all__'
