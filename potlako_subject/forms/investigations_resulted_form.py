from django import forms
# from potlako_validations.form_validators import InvestigationsResultedFormValidator
from ..models import InvestigationsResulted
from .form_mixins import SubjectModelFormMixin


class InvestigationsResultedForm(SubjectModelFormMixin, forms.ModelForm):

#     form_validator_cls = InvestigationsResultedFormValidator

    class Meta:
        model = InvestigationsResulted
        fields = '__all__'
