from django.apps import apps as django_apps
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import eligible_if_yes
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager

from ..choices import ENROLLMENT_SITES
from ..eligibility import Eligibility
from .model_mixins import SearchSlugModelMixin


class EnrollmentManager(SearchSlugManager, models.Manager):

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

    residency = models.CharField(
        verbose_name=('Does the potential participant spend or intend to spend'
                      ' atleast 14 nights per month in the study community?'),
        max_length=3,
        choices=YES_NO)

    nationality = models.CharField(
        verbose_name=("Is the potential participant a Botswana citizen?"),
        max_length=3,
        choices=YES_NO)

    has_diagnosis = models.CharField(
        verbose_name="Is the potential participant a cancer suspect? ",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text="( if 'NO' STOP patient cannot be enrolled )",)

    age_in_years = models.IntegerField(
        verbose_name='Patient age',
        help_text='(Years)',)

    enrollment_site = models.CharField(
        max_length=100,
        null=True,
        choices=ENROLLMENT_SITES,
        help_text="Hospital where subject is recruited")

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

    objects = EnrollmentManager()

    def __str__(self):
        return f'{self.screening_identifier}, {self.subject_identifier}'

    def natural_key(self):
        return (self.subject_identifier,)

    def get_age(self):
        enrollment_cls = django_apps.get_model(self.clinician_enrollment_model)
        try:
            enrollment_obj = enrollment_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except enrollment_cls.DoesNotExist:
            return self.age_in_years
        else:
            return enrollment_obj.age_in_years

    def save(self, *args, **kwargs):
        self.age_in_years = self.get_age()

        eligibility_obj = self.eligibility_cls(
            cancer_status=self.has_diagnosis,
            age_in_years=self.age_in_years)
        self.is_eligible = eligibility_obj.eligible
        if eligibility_obj.reasons_ineligible:
            self.ineligibility = eligibility_obj.reasons_ineligible
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = "Potlako+ Eligibility"
        verbose_name_plural = "Potlako+ Eligibility"
