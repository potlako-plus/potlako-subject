from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators.form_validator_mixin import FormValidatorMixin

from potlako_validations.form_validators import SmsFormValidator
from ..models import SMS


class SMSForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SmsFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SMS
        fields = '__all__'
