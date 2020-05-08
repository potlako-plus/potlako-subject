from django import forms
from potlako_validations.form_validators import SmsFormValidator
from ..models import SMS
from .form_mixins import SubjectModelFormMixin


class SMSForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SmsFormValidator

    class Meta:
        model = SMS
        fields = '__all__'
