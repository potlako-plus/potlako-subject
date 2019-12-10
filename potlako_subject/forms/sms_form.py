from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import SMS


class SMSForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = SMS
        fields = '__all__'
