from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import CancerDiagnosisAndTreatmentAssessmentForm
from ..models import CancerDiagnosisAndTreatmentAssessment

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CancerDiagnosisAndTreatmentAssessment, site=potlako_subject_admin)
class CancerDiagnosisAndTreatmentAssessmentAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CancerDiagnosisAndTreatmentAssessmentForm
