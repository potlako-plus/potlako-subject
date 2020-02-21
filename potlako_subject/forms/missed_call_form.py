from django import forms

from ..models import MissedCall
from .form_mixins import SubjectModelFormMixin


class MissedCallForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MissedCall
        fields = '__all__'
