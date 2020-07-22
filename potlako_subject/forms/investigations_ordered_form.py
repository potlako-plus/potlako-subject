from django import forms
# from potlako_validations.form_validators import InvestigationsOrderedFormValidator
from ..models import InvestigationsOrdered, LabTest
from .form_mixins import SubjectModelFormMixin


class InvestigationsOrderedForm(SubjectModelFormMixin, forms.ModelForm):

#     form_validator_cls = InvestigationsOrderedFormValidator

    class Meta:
        model = InvestigationsOrdered
        fields = '__all__'


class LabTestForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = LabTest
        fields = '__all__'
