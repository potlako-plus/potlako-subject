from django import forms

from ..models import PreviousFacilityVisit
from .form_mixins import SubjectModelFormMixin


class PreviousFacilityVisitForm(SubjectModelFormMixin, forms.ModelForm):

    pass

    class Meta:
        model = PreviousFacilityVisit
        fields = '__all__'
