from django import forms

from potlako_validations.form_validators import MedicalConditionsFormValidator

from ..models import MedicalConditions, MedicalDiagnosis
from .form_mixins import SubjectModelFormMixin


class MedicalDiagnosisForm(SubjectModelFormMixin, forms.ModelForm):

    def clean(self):
        super().clean()

        if not self.data.get(
                'medicalconditions_set-0-medical_condition'):
            raise forms.ValidationError(
                {'Please complete the medical conditions '
                 'table below.'})

    class Meta:
        model = MedicalDiagnosis
        fields = '__all__'


class MedicalConditionsForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MedicalConditionsFormValidator

    class Meta:
        model = MedicalConditions
        fields = '__all__'
