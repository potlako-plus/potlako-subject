from django import forms
from potlako_validations.form_validators import MissedVisitFormValidator
from ..models import MissedVisit
from .form_mixins import SubjectModelFormMixin


class MissedVisitForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MissedVisitFormValidator

    class Meta:
        model = MissedVisit
        fields = '__all__'
