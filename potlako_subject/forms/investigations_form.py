from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Investigations, LabTest


class InvestigationsForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Investigations
        fields = '__all__'


class LabTestForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = LabTest
        fields = '__all__'
