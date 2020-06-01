from django import forms
from potlako_validations.form_validators import PhysicianReviewFormValidator
from ..models import PhysicianReview
from .form_mixins import SubjectModelFormMixin


class PhysicianReviewForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = PhysicianReviewFormValidator

    class Meta:
        model = PhysicianReview
        fields = '__all__'
