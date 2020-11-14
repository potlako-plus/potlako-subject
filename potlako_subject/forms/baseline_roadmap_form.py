from django import forms

from ..models import BaselineRoadMap
from .form_mixins import SubjectModelFormMixin


class BaselineRoadMapForm(SubjectModelFormMixin, forms.ModelForm):

    pass

    class Meta:
        model = BaselineRoadMap
        fields = '__all__'
