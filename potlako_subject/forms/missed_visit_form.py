from django.forms import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import MissedVisit


class MissedVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.Form):

    # form_validator_cls = MissedVisitFormValidator

    class Meta:
        model = MissedVisit
        fields = '__all__'
