from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import SymptomAndcareSeekingAssessmentForm
from ..models import SymptomAndcareSeekingAssessment

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SymptomAndcareSeekingAssessment, site=potlako_subject_admin)
class SymptomAndcareSeekingAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SymptomAndcareSeekingAssessmentForm
