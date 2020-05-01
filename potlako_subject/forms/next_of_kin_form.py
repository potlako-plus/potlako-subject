from django import forms

from ..models import NextOfKin
from .form_mixins import SubjectModelFormMixin


class NextOfKinForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = NextOfKin
        fields = '__all__'
