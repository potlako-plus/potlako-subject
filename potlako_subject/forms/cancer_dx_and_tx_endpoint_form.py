from django import forms

from potlako_validations.form_validators import (
    CancerDxAndTxEndpointFormValidator)

from ..models import CancerDxAndTxEndpoint
from .form_mixins import SubjectModelFormMixin


class CancerDxAndTxAssessmentEndpointForm(
        SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CancerDxAndTxEndpointFormValidator

    class Meta:
        model = CancerDxAndTxEndpoint
        fields = '__all__'
