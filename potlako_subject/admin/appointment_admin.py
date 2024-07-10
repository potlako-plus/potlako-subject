from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from edc_appointment.admin import AppointmentAdmin as BaseAppointmentAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.models import Appointment

from ..forms import AppointmentForm

try:
    edc_appointment_admin.unregister(Appointment)
except NotRegistered:
    pass


@admin.register(Appointment, site=edc_appointment_admin)
class AppointmentAdmin(BaseAppointmentAdmin):

    form = AppointmentForm
