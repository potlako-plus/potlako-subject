from django import forms

from ..models import PatientCallFollowUp
from .form_mixins import SubjectModelFormMixin

from potlako_validations.form_validators import PatientCallFuFormValidator


class PatientCallFollowUpForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = PatientCallFuFormValidator

    class Meta:
        model = PatientCallFollowUp
        fields = '__all__'
