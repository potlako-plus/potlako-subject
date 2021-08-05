from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import InvestigationsResultedForm
from ..models import InvestigationsResulted
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(InvestigationsResulted, site=potlako_subject_admin)
class InvestigationsResultedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InvestigationsResultedForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'tests_resulted_type',
                       'tests_resulted_type_other',
                       'pathology_tests',
                       'imaging_tests',
                       'pathology_specimen_date',
                       'pathology_nhl_date',
                       'pathology_result_date',
                       'pathology_received_date',
                       'pathology_communicated_date',
                       'imaging_tests_date',
                       'specimen_tracking_notes',
                       'diagnosis_results',
                       'diagnosis_results_other',
                       'cancer_type',
                       'diagnoses_made'),
        }), audit_fieldset_tuple)

    radio_fields = {'diagnosis_results': admin.VERTICAL,
                    'results_reviewed': admin.VERTICAL, }

    filter_horizontal = ('tests_resulted_type',)

    conditional_fieldlists = {}

    def get_key(self, request, obj=None):

        usr_groups = [g.name for g in request.user.groups.all()]

        return 'Physician' in usr_groups

    conditional_fieldlists.update(
        {True:
         Insert('results_reviewed', after='diagnoses_made'), })
