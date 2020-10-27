from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import potlako_subject_admin
from ..forms import TransportForm
from ..models import Transport
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Transport, site=potlako_subject_admin)
class TransportAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TransportForm

    fieldsets = (
        (None, {
            'fields': ('subject_visit',
                       'is_criteria_met',
                       'car_ownership',
                       'next_visit_date',
                       'visit_facility',
                       'visit_facility_other',
                       'transport_type',
                       'transport_type_other',
                       'vehicle_status',
                       'vehicle_status_other',
                       'bus_voucher_status',
                       'bus_voucher_status_other',
                       'cash_transfer_status',
                       'cash_transfer_status_other',
                       'criteria_met',
                       'criteria_met_other',
                       'comments',
                       )
        }), audit_fieldset_tuple)

    radio_fields = {
        'is_criteria_met': admin.VERTICAL,
        'car_ownership': admin.VERTICAL,
        'transport_type': admin.VERTICAL,
        'vehicle_status': admin.VERTICAL,
        'bus_voucher_status': admin.VERTICAL,
        'cash_transfer_status': admin.VERTICAL,
    }

    filter_horizontal = ('criteria_met', )

    list_display = ('is_criteria_met',
                    'transport_type')
