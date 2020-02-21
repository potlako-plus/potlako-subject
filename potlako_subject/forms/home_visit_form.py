from django import forms

from ..models import HomeVisit
from .form_mixins import SubjectModelFormMixin


class HomeVisitForm(SubjectModelFormMixin, forms.ModelForm):

    # form_validator_cls = HomeVisitFormValidator

    class Meta:
        model = HomeVisit
        fields = '__all__'
