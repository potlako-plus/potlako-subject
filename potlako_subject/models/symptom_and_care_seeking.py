from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_constants.choices import YES_NO_UNSURE, YES_NO

from .validators import datetime_not_now
from ..choices import DATE_ESTIMATION, REASONS_NOT_DISCUSSED
from ..choices import SYMPTOMS_CONCERN, FACILITY
from .list_models import DiscussionPerson, Symptoms
from .model_mixins import CrfModelMixin


class SymptomAssessmentManager(models.Manager):

    def get_by_natural_key(self, symptom_care_seeking, symptom):
        return self.get(symptom_care_seeking=symptom_care_seeking,
                        symptom=symptom)


class SymptomAndCareSeekingAssessment(CrfModelMixin):
    first_visit_promt = models.TextField(
        verbose_name=('Can you please tell me about what first prompted you to'
                      'go to the clinic, nurse or doctor? Can you describe the '
                      'symptom(s) a bit more? You mentioned (symptoms(s)),were '
                      'there any more symptoms that you noticed about this time?'),
        max_length=100000,
        help_text=('Try identify all participant-reported symptoms first; the checklist'
                   ' comes later'))

    symptoms_cope = models.TextField(
        verbose_name=('What did you do to cope with/help these symptoms?'),
        max_length=100000,
        help_text=('How long did it take before you decided to use any treatment?'
                   'How long did you try for? Did it help at all?'))

    symptoms_present = models.ManyToManyField(
        Symptoms,
        verbose_name=('Now, we\'ve talked about the symptoms that you have described: '
                      'I\'d also like to check whether you had any of the following '
                      'symptoms'),
        blank=True
    )

    symptoms_present_other = models.TextField(
        verbose_name='If other symptoms, please specify',
        max_length=250,
        blank=True,
        null=True)

    symptoms_discussion = models.CharField(
        verbose_name=('Did you discuss your symptoms with anyone before going '
                      'to the clinic?'),
        choices=YES_NO_UNSURE,
        max_length=8)

    reason_no_discussion = models.CharField(
        verbose_name='If no, Why didn\'t you discuss with anyone?',
        choices=REASONS_NOT_DISCUSSED,
        max_length=20,
        blank=True,
        null=True)

    reason_no_discussion_other = OtherCharField()

    discussion_person = models.ManyToManyField(
        DiscussionPerson,
        verbose_name=('If yes, who did you discuss with?'),
        blank=True)

    discussion_person_other = OtherCharField()

    discussion_date = models.DateField(
        verbose_name='When did this discussion take place?',
        validators=[date_not_future, ],
        blank=True,
        null=True)

    discussion_date_estimated = models.CharField(
        verbose_name='Is the discussion date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    discussion_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    medical_advice = models.CharField(
        verbose_name=('If yes, did they encourage you to seek advice from '
                      'clinic?'),
        choices=YES_NO_UNSURE,
        max_length=8,
        blank=True,
        null=True)

    clinic_visit_date = models.DateField(
        verbose_name=('When did you go to a clinic or hospital about these '
                      'symptoms?'),
        validators=[date_not_future, ])

    clinic_visit_date_estimated = models.CharField(
        verbose_name='Is the hospital/clinic visit date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True, )

    clinic_visit_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True, )

    clinic_visited = models.CharField(
        verbose_name='Which clinic or hospital did you go to?',
        choices=FACILITY,
        max_length=32)

    clinic_visited_other = OtherCharField()

    cause_assumption = models.TextField(
        verbose_name='What do you think is causing your symptoms?',
        max_length=1000)

    symptoms_concern = models.CharField(
        verbose_name='How concerned are you about your symptoms?',
        choices=SYMPTOMS_CONCERN,
        max_length=25,
        null=True,
        blank=True, )

    early_symptoms_date = models.DateField(
        verbose_name='Date of earliest onset symptom(s)',
        validators=[date_not_future, datetime_not_now])

    early_symptoms_date_estimated = models.CharField(
        verbose_name='Is the symptoms date estimated?',
        choices=YES_NO,
        max_length=3)

    early_symptoms_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Symptom And Care Seeking Assessment'


class SymptomAssessment(SiteModelMixin, BaseUuidModel):
    symptom_care_seeking = models.ForeignKey(SymptomAndCareSeekingAssessment,
                                             on_delete=PROTECT)

    symptom = models.CharField(
        max_length=50)

    symptom_date = models.DateField(
        validators=[date_not_future, ])

    last_visit_date_estimated = models.CharField(
        verbose_name='Is the symptom date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    last_visit_date_estimation = models.CharField(
        verbose_name='Which part of the date was estimated, if any?',
        choices=DATE_ESTIMATION,
        max_length=15,
        blank=True,
        null=True, )

    history = HistoricalRecords()

    on_site = CurrentSiteManager()

    objects = SymptomAssessmentManager()

    def natural_key(self):
        return (self.symptom,) + self.symptom_care_seeking.natural_key()

    natural_key.dependencies = ['sites.Site']

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Symptom Assessment'
        unique_together = ('symptom_care_seeking', 'symptom')
