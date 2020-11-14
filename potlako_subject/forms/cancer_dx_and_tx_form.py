from django import forms

from potlako_validations.form_validators import (
    CancerDxAndTxFormValidator)

from ..models import CancerDxAndTx
from .form_mixins import SubjectModelFormMixin


class CancerDxAndTxAssessmentForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CancerDxAndTxFormValidator

    class Meta:
        model = CancerDxAndTx
        fields = '__all__'
