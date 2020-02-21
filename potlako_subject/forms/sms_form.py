from django import forms

from ..models import SMS
from .form_mixins import SubjectModelFormMixin


class SMSForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = SMS
        fields = '__all__'
