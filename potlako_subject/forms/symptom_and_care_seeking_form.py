from django import forms

from potlako_validations.form_validators import SymptomAssessmentFormValidator
from potlako_validations.form_validators import SymptomAndCareSeekingFormValidator

from ..models import SymptomAndCareSeekingAssessment, SymptomAssessment
from .form_mixins import SubjectModelFormMixin


class SymptomAndCareSeekingAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SymptomAndCareSeekingFormValidator

    class Meta:
        model = SymptomAndCareSeekingAssessment
        fields = '__all__'


class SymptomAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SymptomAssessmentFormValidator

    class Meta:
        model = SymptomAssessment
        fields = '__all__'
