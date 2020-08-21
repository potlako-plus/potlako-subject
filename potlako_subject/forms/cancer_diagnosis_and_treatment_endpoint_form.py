from django import forms
from ..models import CancerDiagnosisAndTreatmentEndpoint
from .form_mixins import SubjectModelFormMixin


class CancerDiagnosisAndTreatmentAssessmentEndpointForm(
        SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CancerDiagnosisAndTreatmentEndpoint
        fields = '__all__'
