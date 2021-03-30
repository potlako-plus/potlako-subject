from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import ModelAdminNextUrlRedirectError, audit_fieldset_tuple
from ..admin_site import potlako_subject_admin
from ..forms import PatientAvailabilityLogEntryForm
from ..models import PatientAvailabilityLogEntry, PatientAvailabilityLog
from .modeladmin_mixins import ModelAdminMixin


@admin.register(PatientAvailabilityLogEntry, site=potlako_subject_admin)
class PatientAvailabilityLogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PatientAvailabilityLogEntryForm

    fieldsets = (
        (None, {
            'fields': [
                'patient_availability_log',
                'report_datetime',
                'can_take_call',
                'reason',
                'reason_other',
                'comment',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'can_take_call': admin.VERTICAL,
        'reason': admin.VERTICAL}

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['patient_availability_log'].queryset = \
            PatientAvailabilityLog.objects.filter(id=request.GET.get('patient_availability_log'))
        return super(PatientAvailabilityLogEntryAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = settings.DASHBOARD_URL_NAMES.get(
                'screening_listboard_url')
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url
