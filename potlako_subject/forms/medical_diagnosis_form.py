from django import forms
from ..models import MedicalConditions, MedicalDiagnosis
from .form_mixins import SubjectModelFormMixin


class MedicalDiagnosisForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MedicalDiagnosis
        fields = '__all__'


class MedicalConditionsForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MedicalConditions
        fields = '__all__'
