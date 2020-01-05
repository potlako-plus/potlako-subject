from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'potlako_subject'
    verbose_name = 'Potlako Subject CRFs'
    admin_site_name = 'potlako_subject_admin'

    def ready(self):
        from .models import subject_consent_on_post_save
