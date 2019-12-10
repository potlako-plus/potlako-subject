from django import forms
from edc_form_validators import FormValidatorMixin
from edc_base.sites import SiteModelFormMixin

from ..models import HomeVisit


class HomeVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    # form_validator_cls = HomeVisitFormValidator

    class Meta:
        model = HomeVisit
        fields = '__all__'
