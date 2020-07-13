from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from potlako_validations.form_validators import ScreeningFormValidator
from ..models import SubjectScreening


class SubjectScreeningForm(SiteModelFormMixin, FormValidatorMixin,
                           forms.ModelForm):

    form_validator_cls = ScreeningFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SubjectScreening
        fields = '__all__'
