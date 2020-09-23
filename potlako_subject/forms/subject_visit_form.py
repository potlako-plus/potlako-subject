from django import forms
from django.apps import apps as django_apps
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import OTHER
from edc_form_validators import FormValidatorMixin
from edc_form_validators.base_form_validator import INVALID_ERROR
from edc_visit_tracking.constants import UNSCHEDULED, MISSED_VISIT
from edc_visit_tracking.form_validators import (
    VisitFormValidator as BaseVisitFormValidator)
from edc_appointment.constants import IN_PROGRESS_APPT

from ..models import SubjectVisit


class VisitFormValidator(BaseVisitFormValidator):
    
    @property
    def appointment_cls(self):
        return django_apps.get_model('edc_appointment.appointment')

    def validate_visit_code_sequence_and_reason(self):
        appointment = self.cleaned_data.get('appointment')
        reason = self.cleaned_data.get('reason')
        if appointment:
            if appointment.visit_code_sequence == 0 :
                
                reasons = ['missed_quarterly_visit', 'quarterly_visit/contact',
                       'lost_to_follow_up']
                
                if(appointment.visit_code == '1000' and reason in reasons):
                    raise forms.ValidationError({
                    'reason': 'Invalid visit reason'},
                    code=INVALID_ERROR)
                if reason == 'unscheduled_visit/contact':
                    raise forms.ValidationError({
                    'reason': 'This can not be an unscheduled visit/contact.'})
            else:
                if reason == 'initial_visit/contact':
                    raise forms.ValidationError({
                        'reason': 'This can not be an initial visit/contact.'})
                
        in_progress_count = self.appointment_cls.objects.filter(
            subject_identifier=appointment.subject_identifier,
            appt_status=IN_PROGRESS_APPT).count()
        
        if in_progress_count > 1:
            raise forms.ValidationError('There is more than one appointment in progress. '
                                        'Cannot proceed.')

    def validate_required_fields(self):

        self.required_if(
            MISSED_VISIT,
            field='reason',
            field_required='reason_missed')

        self.required_if(
            'unscheduled_visit/contact',
            field='reason',
            field_required='reason_unscheduled')

        self.required_if(
            OTHER,
            field='info_source',
            field_required='info_source_other')

        self.required_if(
            OTHER,
            field='reason_unscheduled',
            field_required='reason_unscheduled_other')

    def validate_survival_status_if_alive(self):
        pass


class SubjectVisitForm (
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = VisitFormValidator

    class Meta:
        model = SubjectVisit
        fields = '__all__'
