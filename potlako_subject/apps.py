from datetime import datetime
from dateutil.tz import gettz

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'potlako_subject'
    verbose_name = 'Potlako+ Subject CRFs'
    admin_site_name = 'potlako_subject_admin'

    def ready(self):
        from .models import subject_consent_on_post_save
        from .models import patient_call_initial_on_post_save
        from .models import patient_call_followup_on_post_save
        from .models import subject_visit_on_post_save
        from .models import home_visit_on_post_save
        from .models import missed_call_on_post_save


if settings.APP_NAME == 'potlako_subject':
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_device.constants import CENTRAL_SERVER, CLIENT, NODE_SERVER
    from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
    from edc_device.device_permission import DevicePermissions
    from edc_device.device_permission import DeviceAddPermission, DeviceChangePermission
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
    from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT
    from edc_visit_tracking.apps import (
        AppConfig as BaseEdcVisitTrackingAppConfig)
    from edc_sms.apps import AppConfig as BaseEdcSmsAppConfig


    class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
        use_settings = True
        device_permissions = DevicePermissions(
            DeviceAddPermission(
                model='plot.plot',
                device_roles=[CENTRAL_SERVER, CLIENT]),
            DeviceChangePermission(
                model='plot.plot',
                device_roles=[NODE_SERVER, CENTRAL_SERVER, CLIENT]))


    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'potlako_subject': (
                'subject_visit', 'potlako_subject.subjectvisit')}


    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = 'BHP132'
        protocol_number = '132'
        protocol_name = 'Potlako Plus'
        protocol_title = ''
        study_open_datetime = datetime(
            2016, 4, 1, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2025, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        default_appt_type = 'clinic'
        apply_community_filter = True
        send_sms_reminders = True
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='potlako_subject.subjectvisit')
        ]


    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {'potlako_subject.subjectvisit': 'reason'}
        other_visit_reasons = ['off study', 'deferred', 'death']
        other_create_visit_reasons = [
            'initial_visit/contact', 'fu_visit/contact',
            'missed_visit', 'unscheduled_visit/contact']
        create_on_reasons = [SCHEDULED, UNSCHEDULED] + other_create_visit_reasons
        delete_on_reasons = [LOST_VISIT] + other_visit_reasons


    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}


    class EdcSmsAppConfig(BaseEdcSmsAppConfig):
        locator_model = 'potlako_subject.subjectlocator'
        consent_model = 'potlako_subject.subjectconsent'
        sms_model = 'potlako_subject.sms'
