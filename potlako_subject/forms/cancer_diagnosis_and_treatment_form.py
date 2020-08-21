from django import forms
from ..models import CancerDiagnosisAndTreatmentAssessment
from .form_mixins import SubjectModelFormMixin


class CancerDiagnosisAndTreatmentAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

#     form_validator_cls = None

    class Meta:
        model = CancerDiagnosisAndTreatmentAssessment
        fields = '__all__'
