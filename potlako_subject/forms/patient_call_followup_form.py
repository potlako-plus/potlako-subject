from django import forms
from edc_constants.constants import YES
from ..models import PatientCallFollowUp
from .form_mixins import SubjectModelFormMixin

from potlako_validations.form_validators import PatientCallFuFormValidator


class PatientCallFollowUpForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = PatientCallFuFormValidator

    def clean(self):
        cleaned_data = super().clean()

        interval_visit_date = self.data.get(
            'facilityvisit_set-0-interval_visit_date')

        if (cleaned_data.get('interval_visit') == YES and not interval_visit_date):
            raise forms.ValidationError(
                {'interval_visit': 'Please complete the facility visit '
                 'table below.'})

    class Meta:
        model = PatientCallFollowUp
        fields = '__all__'
