from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import PhysicianReview


class PhysicianReviewForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    # form_validator_cls

    class Meta:
        model = PhysicianReview
        fields = '__all__'
