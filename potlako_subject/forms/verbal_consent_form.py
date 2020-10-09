from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import VerbalConsent


class VerbalConsentForm(SiteModelFormMixin, forms.ModelForm):

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = VerbalConsent
        fields = '__all__'
