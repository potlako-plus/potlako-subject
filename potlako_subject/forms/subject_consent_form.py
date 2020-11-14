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
    
    language = forms.ChoiceField(
        label='Language of consent', 
        choices=settings.LANGUAGES,
        widget=forms.Select(attrs={'disabled':'disabled'}))

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    language = forms.CharField(
        label='Language of consent',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.cleaned_data['study_site'] = settings.DEFAULT_STUDY_SITE
        self.cleaned_data['report_datetime'] = self.cleaned_data.get('consent_datetime')
        super().clean()

    class Meta:
        model = SubjectConsent
        fields = '__all__'
