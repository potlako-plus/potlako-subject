from django import forms
from django.conf import settings
from edc_base.sites import SiteModelFormMixin
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin

from potlako_validations.form_validators import SubjectConsentFormValidator

from ..models import SubjectConsent


class SubjectConsentForm(
        SiteModelFormMixin, FormValidatorMixin, ConsentModelFormMixin,
        forms.ModelForm):

    form_validator_cls = SubjectConsentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def clean(self):
        self.cleaned_data['study_site'] = settings.DEFAULT_STUDY_SITE
        super().clean()

    class Meta:
        model = SubjectConsent
        fields = '__all__'
