from django import forms
from potlako_validations.form_validators import FacilityVisitFormValidator
from ..models import FacilityVisit
from .form_mixins import SubjectModelFormMixin


class FacilityVisitForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = FacilityVisitFormValidator

    class Meta:
        model = FacilityVisit
        fields = '__all__'
