from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import Transport


class TransportForm(
        SiteModelFormMixin, FormValidatorMixin, forms.Form):

    # form_validator_cls = TransportFormValidator

    class Meta:
        model = Transport
        fields = '__all__'
