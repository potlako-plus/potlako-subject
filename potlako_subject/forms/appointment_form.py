from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_metadata.constants import REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from edc_appointment.constants import COMPLETE_APPT
from edc_appointment.form_validators import AppointmentFormValidator
from edc_appointment.models import Appointment

from ..models import SubjectVisit


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin,
                      AppointmentFormValidator, forms.ModelForm):
    """ Note, the appointment is only changed, never added, through this form.
    """

    def clean(self):
        super().clean()
        self.validate_appt_complete()

    @property
    def crf_metadata_required_exists(self):
        """Returns True if any required CRFs for this visit code have
        not yet been keyed.
        """
        return CrfMetadata.objects.filter(
            subject_identifier=self.instance.subject_identifier,
            visit_schedule_name=self.instance.visit_schedule_name,
            schedule_name=self.instance.schedule_name,
            visit_code=self.instance.visit_code,
            visit_code_sequence=self.instance.visit_code_sequence,
            entry_status=REQUIRED).exists()

    @property
    def requisition_metadata_required_exists(self):
        """Returns True if any required requisitions for this visit code
        have not yet been keyed.
        """
        return RequisitionMetadata.objects.filter(
            subject_identifier=self.instance.subject_identifier,
            visit_schedule_name=self.instance.visit_schedule_name,
            schedule_name=self.instance.schedule_name,
            visit_code=self.instance.visit_code,
            visit_code_sequence=self.instance.visit_code_sequence,
            entry_status=REQUIRED).exists()

    def validate_appt_complete(self):
        appt_status = self.cleaned_data.get('appt_status')

        if appt_status == COMPLETE_APPT:
            try:
                SubjectVisit.objects.get(appointment=self.instance)
            except SubjectVisit.DoesNotExist:
                raise forms.ValidationError(
                    {'appt_status':
                     'There is no visit completed, can not set status as done.'})

    class Meta:
        model = Appointment
        fields = '__all__'
