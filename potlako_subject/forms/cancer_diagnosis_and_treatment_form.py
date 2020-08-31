from django import forms

from potlako_validations.form_validators import (
    CancerDiagnosisAndTreatmentFormValidator)

from ..models import CancerDiagnosisAndTreatmentAssessment
from .form_mixins import SubjectModelFormMixin


class CancerDiagnosisAndTreatmentAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CancerDiagnosisAndTreatmentFormValidator

    class Meta:
        model = CancerDiagnosisAndTreatmentAssessment
        fields = '__all__'
