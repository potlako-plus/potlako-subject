from django import forms

from potlako_validations.form_validators import SymptomsAndCareSeekingEndpointFormValidator
from django.core.exceptions import ValidationError
from ..models import SymptomsAndCareSeekingEndpoint
from .form_mixins import SubjectModelFormMixin
from django.apps import apps as django_apps

class SymptomAndCareSeekingEndpointForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SymptomsAndCareSeekingEndpointFormValidator
    symptoms_and_care_seeking_model = 'potlako_subject.symptomandcareseekingassessment'

    @property
    def symptoms_and_care_seeking_cls(self):
        return django_apps.get_model(self.symptoms_and_care_seeking_model)
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        subject_identifier =  self.initial.get('subject_identifier', None)
        instance = kwargs.get("instance")
    

        if subject_identifier:
            try:
                symptoms_and_care_seeking_obj = self.symptoms_and_care_seeking_cls.objects.get(
                    subject_visit__subject_identifier = subject_identifier
                )
            except self.symptoms_and_care_seeking_cls.DoesNotExist:
                raise ValidationError('Symptom and Care seeking Assessment does not exist.')
            else:
                if instance == None:
                    self.initial['cancer_symptom_date'] = symptoms_and_care_seeking_obj.early_symptoms_date
                    self.initial['cancer_symptom_estimated'] = symptoms_and_care_seeking_obj.early_symptoms_date_estimated 
                    self.initial['cancer_symptom_estimation'] = symptoms_and_care_seeking_obj.early_symptoms_date_estimation

    class Meta:
        model = SymptomsAndCareSeekingEndpoint
        fields = '__all__'
