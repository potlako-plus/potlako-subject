from django import forms

from potlako_validations.form_validators import MedicalConditionsFormValidator

from ..models import MedicalConditions, MedicalDiagnosis
from .form_mixins import SubjectModelFormMixin


class MedicalDiagnosisForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MedicalDiagnosis
        fields = '__all__'


class MedicalConditionsForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MedicalConditionsFormValidator

    class Meta:
        model = MedicalConditions
        fields = '__all__'
