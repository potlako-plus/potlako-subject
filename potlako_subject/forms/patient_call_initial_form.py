from django import forms
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES

from potlako_validations.form_validators import PatientCallInitialFormValidator
from ..models import PatientCallInitial
from .form_mixins import SubjectModelFormMixin


class PatientCallInitialForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = PatientCallInitialFormValidator

    def clean(self):
        cleaned_data = super().clean()

        self.validate_date_is_future()

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

    def validate_date_is_future(self):
        """Validate that the date is a future date if it is being changed"""

        if self.instance:
            if(self.instance.next_appointment_date != self.cleaned_data.get('next_appointment_date')
                    and self.cleaned_data.get('next_appointment_date') < get_utcnow().date()):
                raise forms.ValidationError({'next_appointment_date': 'Expected a future date'})

        elif self.cleaned_data.get('next_appointment_date') < get_utcnow().date():
            raise forms.ValidationError({'next_appointment_date': 'Expected a future date'})

    class Meta:
        model = PatientCallInitial
        fields = '__all__'
