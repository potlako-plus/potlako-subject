from django import forms

from potlako_validations.form_validators import (
    CancerDiagnosisAndTreatmentEndpointFormValidator)

from ..models import CancerDiagnosisAndTreatmentEndpoint
from .form_mixins import SubjectModelFormMixin


class CancerDiagnosisAndTreatmentAssessmentEndpointForm(
        SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CancerDiagnosisAndTreatmentEndpointFormValidator

    class Meta:
        model = CancerDiagnosisAndTreatmentEndpoint
        fields = '__all__'
