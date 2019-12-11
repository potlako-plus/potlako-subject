from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import MissedCall


class MissedCallForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = MissedCall
        fields = '__all__'
