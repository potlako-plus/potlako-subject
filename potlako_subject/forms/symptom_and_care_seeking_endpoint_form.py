from django import forms
from ..models import SymptomsAndCareSeekingEndpointRecording
from .form_mixins import SubjectModelFormMixin


class SymptomAndcareSeekingEndpointForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = SymptomsAndCareSeekingEndpointRecording
        fields = '__all__'
