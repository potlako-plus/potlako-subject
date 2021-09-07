from django import forms
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from ..models import PatientCallFollowUp
from .form_mixins import SubjectModelFormMixin

from potlako_validations.form_validators import PatientCallFuFormValidator


class PatientCallFollowUpForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = PatientCallFuFormValidator

    def clean(self):
        cleaned_data = super().clean()

        self.validate_date_is_future()

        interval_visit_date = self.data.get(
            'facilityvisit_set-0-interval_visit_date')

        if (cleaned_data.get('interval_visit') == YES and not interval_visit_date):
            raise forms.ValidationError(
                {'interval_visit': 'Please complete the facility visit '
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
        model = PatientCallFollowUp
        fields = '__all__'
