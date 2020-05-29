from django import forms
from potlako_validations.form_validators import ClinicianCallFollowupFormValidator
from ..models import ClinicianCallFollowUp
from .form_mixins import SubjectModelFormMixin


class ClinicianCallFollowUpForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = ClinicianCallFollowupFormValidator

    class Meta:
        model = ClinicianCallFollowUp
        fields = '__all__'
