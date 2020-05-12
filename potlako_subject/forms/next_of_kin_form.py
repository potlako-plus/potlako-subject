from django import forms

from potlako_validations.form_validators import NextOfKinFormValidator

from ..models import NextOfKin
from .form_mixins import SubjectModelFormMixin


class NextOfKinForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = NextOfKinFormValidator

    class Meta:
        model = NextOfKin
        fields = '__all__'
