from django import forms

from potlako_validations.form_validators import SymptomsAndCareSeekingEndpointFormValidator

from ..models import SymptomsAndCareSeekingEndpointRecording
from .form_mixins import SubjectModelFormMixin


class SymptomAndCareSeekingEndpointForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SymptomsAndCareSeekingEndpointFormValidator

    class Meta:
        model = SymptomsAndCareSeekingEndpointRecording
        fields = '__all__'
