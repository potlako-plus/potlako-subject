from django import forms
from potlako_validations.form_validators import InvestigationsFormValidator
from ..models import Investigations, LabTest
from .form_mixins import SubjectModelFormMixin


class InvestigationsForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = InvestigationsFormValidator

    class Meta:
        model = Investigations
        fields = '__all__'


class LabTestForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = LabTest
        fields = '__all__'
