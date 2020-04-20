from django import forms

from ..models import FacilityVisit
from .form_mixins import SubjectModelFormMixin


class FacilityVisitForm(SubjectModelFormMixin, forms.ModelForm):

    pass

    class Meta:
        model = FacilityVisit
        fields = '__all__'
