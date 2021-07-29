from django.apps import apps as django_apps
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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

        return queryset.filter(screening_identifier__in=clinician_call_enrol_ids)
