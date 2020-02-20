from django.contrib import admin

from ..admin_site import potlako_subject_admin
from ..forms import ExitFromStudyForm
from ..models import ExitFromStudy


@admin.register(ExitFromStudy, site=potlako_subject_admin)
class ExitFromStudyAdmin(admin.ModelAdmin):

    form = ExitFromStudyForm

    fieldsets = (
        ('Fields to be completed by Potlako Research Assistant (Deaths/LTFU)',
            {
                'fields': ('exit_reason',
                           'general_comments',
                           'last_visit_date',
                           'last_visit_facility',
                           'death_date',
                           'cause_of_death',
                           'place_of_death',
                           'facility_patient_died',
                           'death_info_source',
                           'info_source_other',
                           'ltfu_criteria_met',
                           'new_kgotla_res',
                           'new_village_res',
                           'new_district_res',
                           'new_facility_name',
                           'new_facility_type',
                           'exit_hiv_status',
                           'latest_hiv_test_known',
                           'hiv_test_date',
                           'review_flag'),
            }),
        ('Fields to be completed by Physician (Final status)', {
            'fields': ('components_rec',
                       'components_rec_other',
                       'cancer_treatment_rec',
                       'treatment_intent',
                       'date_therapy_started'),
        }),
    )

    radio_fields = {'exit_reason': admin.VERTICAL,
                    'last_visit_facility': admin.VERTICAL,
                    'place_of_death': admin.VERTICAL,
                    'facility_patient_died': admin.VERTICAL,
                    'death_info_source': admin.VERTICAL,
                    'ltfu_criteria_met': admin.VERTICAL,
                    'new_district_res': admin.VERTICAL,
                    'new_facility_type': admin.VERTICAL,
                    'exit_hiv_status': admin.VERTICAL,
                    'latest_hiv_test_known': admin.VERTICAL,
                    'review_flag': admin.VERTICAL,
                    'components_rec': admin.VERTICAL,
                    'cancer_treatment_rec': admin.VERTICAL,
                    'treatment_intent': admin.VERTICAL, }
