from potlako_subject.action_items import SUBJECT_LOCATOR_ACTION

from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_crypto_fields.fields import EncryptedCharField
from edc_action_item.model_mixins import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import TelephoneNumber
from edc_base.model_validators import date_not_future
from edc_base.model_validators.phone import CellNumber
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import OPEN, CLOSED
from edc_locator.model_mixins import LocatorModelMixin, LocatorManager

from ..choices import YES_NO_DW


class SubjectLocator(LocatorModelMixin, RequiresConsentFieldsModelMixin,
                     ActionModelMixin, SiteModelMixin, BaseUuidModel):
    """A model completed by the user to that captures participant
    locator information and permission to contact.
    """

    action_name = SUBJECT_LOCATOR_ACTION

    tracking_identifier_prefix = 'SL'

    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, null=True, editable=False,
        related_name='subject_locator_site')

    date_signed = models.DateField(
        verbose_name="Date Locator Form signed ",
        default=timezone.now,
        validators=[date_not_future, ],
    )

    local_clinic = models.CharField(
        verbose_name=(
            "Which health facility do you normally go to, in this village?"),
        max_length=75,
        help_text="Please give clinic code.",
    )
    home_village = models.CharField(
        verbose_name=("Where is your home village?"),
        max_length=75,
    )

    has_alt_contact = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name=("If we are unable to contact the person indicated above,"
                      " is there another individual (including next of kin) "
                      "with whom the study team can get in contact with?"),
    )

    alt_contact_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full Name of the responsible person",
        help_text="include firstname and lastname",
        blank=True,
        null=True,
    )

    alt_contact_rel = EncryptedCharField(
        max_length=35,
        verbose_name="Relationship to participant",
        blank=True,
        null=True,
    )
    alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[CellNumber, ],
        blank=True,
        null=True,
    )

    other_alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[CellNumber, ],
        blank=True,
        null=True,
    )

    alt_contact_tel = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[TelephoneNumber, ],
        blank=True,
        null=True,
    )

    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO_DW,
        verbose_name=mark_safe(
            'Has the participant given permission to contacted <b>at work</b> '
            'by telephone or cell by study staff for follow-up purposes '
            'during the study?'))

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = LocatorManager()

    def save(self, *args, **kwargs):
        # Close data action item if locator information is updated
        self.close_data_action_item()
        super().save(*args, **kwargs)

    def __str__(self):
        return (f'{self.subject_identifier}')

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    def close_data_action_item(self):
        """ Update locator data action item to closed once the locator
            information has been updated.
        """
        data_action_item_cls = django_apps.get_model(
            'edc_data_manager.dataactionitem')
        try:
            action_item = data_action_item_cls.objects.get(
                subject_identifier=self.subject_identifier,
                subject='*Update the subject locator information*',
                status=OPEN)
        except data_action_item_cls.DoesNotExist:
            pass
        else:
            if self.modified.date() >= action_item.action_date:
                action_item.status = CLOSED
                action_item.save()
            
    class Meta:
        verbose_name = 'Subject Locator'
