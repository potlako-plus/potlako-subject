from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import ModelAdminNextUrlRedirectError

from ..admin_site import potlako_subject_admin
from ..forms import SymptomAndCareSeekingEndpointForm
from ..models import SymptomsAndCareSeekingEndpoint
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SymptomsAndCareSeekingEndpoint, site=potlako_subject_admin)
class SymptomAndCareSeekingEndpointAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SymptomAndCareSeekingEndpointForm
    extra_context_models = ['cliniciancallenrollment',
                            'baselineclinicalsummary',
                            'symptomandcareseekingassessment']

    fieldsets = (
        (None, {
            'fields': ('subject_identifier',
                       'cancer_symptom_date',
                       'cancer_symptom_estimated',
                       'cancer_symptom_estimation',
                       'discussion_date',
                       'discussion_date_estimated',
                       'discussion_date_estimation',
                       'seek_help_date',
                       'seek_help_date_estimated',
                       'seek_help_date_estimation',
                       'first_seen_date',
                       'first_seen_date_estimated',
                       'first_seen_date_estimation'),
        }), audit_fieldset_tuple)

    radio_fields = {'cancer_symptom_estimated': admin.VERTICAL,
                    'cancer_symptom_estimation': admin.VERTICAL,
                    'discussion_date_estimated': admin.VERTICAL,
                    'discussion_date_estimation': admin.VERTICAL,
                    'seek_help_date_estimated': admin.VERTICAL,
                    'seek_help_date_estimation': admin.VERTICAL,
                    'first_seen_date_estimated': admin.VERTICAL,
                    'first_seen_date_estimation': admin.VERTICAL,
                    }

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = settings.DASHBOARD_URL_NAMES.get('endpoint_listboard_url')
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url
