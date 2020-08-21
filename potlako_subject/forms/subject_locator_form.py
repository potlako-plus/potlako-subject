from django import forms
from edc_form_validators import FormValidatorMixin

from potlako_validations.form_validators import SubjectLocatorFormValidator

from ..models import SubjectLocator


class SubjectLocatorForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectLocatorFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SubjectLocator
        fields = '__all__'
