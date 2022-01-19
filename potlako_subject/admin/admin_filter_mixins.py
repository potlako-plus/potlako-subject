from django.apps import apps as django_apps
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from edc_constants.choices import YES_NO

from ..choices import ENROLLMENT_SITES


class FacilityListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Facility')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'facility'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ENROLLMENT_SITES

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        clinician_enrollment_cls = django_apps.get_model(
            'potlako_subject.cliniciancallenrollment')

        clinician_call_enrol_ids = clinician_enrollment_cls.objects.values_list(
            'screening_identifier', flat=True).filter(facility=self.value())

        if clinician_call_enrol_ids:

            return queryset.filter(
                screening_identifier__in=clinician_call_enrol_ids)
        else:
            return queryset


class CancerTreatmentFilter(admin.SimpleListFilter):
    title = _('Cancer Treatment')

    parameter_name = 'cancer_treatment'

    def lookups(self, request, model_admin):
        return YES_NO

    def queryset(self, request, queryset):
        cancer_dx_and_tx_cls = django_apps.get_model(
            'potlako_subject.cancerdxandtx'
        )

        cancer_dx_and_tx_ids = cancer_dx_and_tx_cls.objects.values_list(
            'cancer_treatment', flat=True).filter(
            cancer_treatment=self.value())

        if cancer_dx_and_tx_ids:

            return queryset.filter(
                cancer_treatment__in=cancer_dx_and_tx_ids)
        else:
            return queryset
