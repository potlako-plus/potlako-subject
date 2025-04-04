from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager

from ..choices import ENROLLMENT_SITES, DISINTEREST_REASON, YES_NO_DECEASED
from ..eligibility import Eligibility
from .model_mixins import SearchSlugModelMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE


class SubjectScreeningManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(
            screening_identifier=screening_identifier
        )


class SubjectScreening(
        NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
        SearchSlugModelMixin, BaseUuidModel):

    eligibility_cls = Eligibility

    clinician_enrollment_model = 'potlako_subject.cliniciancallenrollment'

    screening_identifier = models.CharField(
        verbose_name="Screening Identifier",
        max_length=36,
        unique=True,)

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        help_text='Date and time of report.')

    enrollment_interest = models.CharField(
        verbose_name=('Does the patient want to be enrolled into the'
                      ' study?'),
        max_length=8,
        choices=YES_NO_DECEASED)

    unknown_reason = models.CharField(
        verbose_name='If unknown, state reason',
        max_length=50,
        null=True,
        blank=True
    )

    disinterest_reason = models.CharField(
        verbose_name=('If no, reason patient does not wish to enroll'
                      ' into the study'),
        max_length=50,
        choices=DISINTEREST_REASON,
        null=True,
        blank=True)

    disinterest_reason_other = OtherCharField()

    residency = models.CharField(
        verbose_name=('Does the potential participant spend or intend to spend'
                      ' atleast 14 nights per month in the study community?'),
        max_length=3,
        default=NOT_APPLICABLE,
        choices=YES_NO_NA)

    nationality = models.CharField(
        verbose_name=("Is the potential participant a Botswana citizen?"),
        max_length=3,
        default=NOT_APPLICABLE,
        choices=YES_NO_NA)

    has_diagnosis = models.CharField(
        verbose_name="Is the potential participant a cancer suspect? ",
        max_length=3,
        choices=YES_NO,
        help_text="( if 'NO' STOP patient cannot be enrolled )",)

    age_in_years = models.IntegerField(
        verbose_name='Patient age',
        help_text='(Years)',)

    enrollment_site = models.CharField(
        max_length=50,
        null=True,
        choices=ENROLLMENT_SITES,
        help_text="Hospital where subject is recruited")

    enrollment_site_other = OtherCharField()

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = SubjectScreeningManager()

    def __str__(self):
        return f'{self.screening_identifier}, {self.subject_identifier}'

    def natural_key(self):
        return (self.screening_identifier,)

    def get_age(self):
        enrollment_cls = django_apps.get_model(self.clinician_enrollment_model)
        try:
            enrollment_obj = enrollment_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except enrollment_cls.DoesNotExist:
            return self.age_in_years
        else:
            return enrollment_obj.age_in_years

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['screening_identifier', ])
        return fields

    def save(self, *args, **kwargs):
        self.age_in_years = self.get_age()
        eligibility_obj = self.eligibility_cls(
            cancer_status=self.has_diagnosis,
            age_in_years=self.age_in_years,
            residency=self.residency,
            nationality=self.nationality,
            enrollment_interest=self.enrollment_interest,
            unknown_reason=self.unknown_reason)
        self.is_eligible = eligibility_obj.is_eligible
        if eligibility_obj.reasons_ineligible:
            self.ineligibility = eligibility_obj.reasons_ineligible
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = "Potlako+ Eligibility"
        verbose_name_plural = "Potlako+ Eligibility"
