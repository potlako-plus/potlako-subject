from django.contrib import admin
from ..admin_site import potlako_subject_admin
from ..forms import TransportForm
from ..models import Transport


@admin.register(Transport, site=potlako_subject_admin)
class TransportAdmin(admin.ModelAdmin):

    form = TransportForm

    fieldsets = (
        (None, {
            'fields': ('report_datetime',
                       'is_criteria_met',
                       'qualification',
                       'housemate',
                       'car_ownership',
                       'criteria_met',
                       'next_visit_date',
                       'visit_facility',
                       'transport_type',
                       'facility_vehicle_status',
                       'vehicle_status_other',
                       'vehicle_request_date',
                       'facility_personnel',
                       'bus_voucher_status',
                       'bus_status_other',
                       'cash_transfer_status',
                       'cash_status_other',
                       'comments',
                       )
        }),
    )

    radio_fields = {
        'is_criteria_met': admin.VERTICAL,
        'housemate': admin.VERTICAL,
        'car_ownership': admin.VERTICAL,
        'criteria_met': admin.VERTICAL,
        'visit_facility': admin.VERTICAL,
        'transport_type': admin.VERTICAL,
        'facility_vehicle_status': admin.VERTICAL,
        'bus_voucher_status': admin.VERTICAL,
        'cash_transfer_status': admin.VERTICAL,
    }

    list_display = ('report_datetime', 'is_criteria_met',
                    'criteria_met', 'transport_type')
