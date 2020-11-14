from django import forms
from edc_constants.constants import NO, YES

from potlako_validations.form_validators import PatientCallInitialFormValidator
from ..models import PatientCallInitial
from .form_mixins import SubjectModelFormMixin


class PatientCallInitialForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = PatientCallInitialFormValidator

    def clean(self):
        cleaned_data = super().clean()

        previous_facility_visit = self.data.get(
            'previousfacilityvisit_set-0-facility_visited')

        if (cleaned_data.get('other_facility') == NO
                and previous_facility_visit):
            raise forms.ValidationError(
                {'other_facility': 'The previous facility '
                 'table below is not required.'})
        elif (cleaned_data.get('other_facility') == YES
                and not previous_facility_visit):
            raise forms.ValidationError(
                {'other_facility': 'Please complete the previous facility '
                 'table below.'})

    class Meta:
        model = PatientCallInitial
        fields = '__all__'
