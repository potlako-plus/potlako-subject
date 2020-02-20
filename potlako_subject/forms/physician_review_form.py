from django import forms

from ..models import PhysicianReview
from .form_mixins import SubjectModelFormMixin


class PhysicianReviewForm(SubjectModelFormMixin, forms.ModelForm):

    # form_validator_cls

    class Meta:
        model = PhysicianReview
        fields = '__all__'
