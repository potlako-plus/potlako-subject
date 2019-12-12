from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import PatientStatus


class PatientStatusForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = PatientStatus
        fields = '__all__'
