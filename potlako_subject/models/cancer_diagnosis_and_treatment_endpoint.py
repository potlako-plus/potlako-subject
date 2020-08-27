from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..choices import CANCER_EVALUATION, CLINICAL_IMPRESSION, CANCER_DIAGNOSIS
from ..choices import METASTASIS_STAGES, STAGES, TREATMENT_INTENT
from ..choices import NON_CANCER_DIAGNOSIS, DATE_ESTIMATION, CANCER_DIAGNOSIS_STAGE
from .model_mixins import CrfModelMixin
from edc_base.sites import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel


class CancerDiagnosisAndTreatmentEndpoint(SiteModelMixin, BaseUuidModel):

    cancer_evaluation = models.CharField(
        max_length=30,
        choices=CANCER_EVALUATION)

    diagnosis_date = models.DateField(
        verbose_name='If complete, date of final diagnosis',
        blank=True,
        null=True)

    diagnosis_date_estimated = models.CharField(
        verbose_name='Is the diagnosis date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    diagnosis_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    clinical_impression = models.CharField(
        verbose_name='Final Clinical Impression',
        max_length=30,
        choices=CLINICAL_IMPRESSION,
        blank=True,
        null=True)

    final_cancer_diagnosis = models.CharField(
        verbose_name='If confirmed/probable cancer, final cancer diagnosis',
        max_length=30,
        choices=CANCER_DIAGNOSIS,
        null=True,
        blank=True)

    final_cancer_diagnosis_other = OtherCharField(
        verbose_name='Final Cancer Diagnosis, Other',
        max_length=30)

    non_cancer_diagnosis = models.CharField(
        verbose_name='Final Non-Cancer diagnosis',
        choices=NON_CANCER_DIAGNOSIS,
        max_length=25,
        blank=True,
        null=True)

    non_cancer_diagnosis_other = OtherCharField(
        verbose_name='Final Non-Cancer Diagnosis, Other',
        max_length=30)

    cancer_diagnosis = models.CharField(
        verbose_name='Cancer diagnosis',
        # choices=to be provided
        max_length=2,
        blank=True,
        null=True)

    cancer_histology_code = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2999)],
        blank=True,
        null=True)

    cancer_diagnosis_stage = models.CharField(
        verbose_name='Cancer stage at diagnosis',
        choices=CANCER_DIAGNOSIS_STAGE,
        max_length=15,
        blank=True,
        null=True)

    tumor_stage = models.IntegerField(
        verbose_name='AJCC tumor stage',
        choices=STAGES,
        blank=True,
        null=True)

    nodal_stage = models.IntegerField(
        verbose_name='AJCC nodal stage',
        choices=STAGES,
        blank=True,
        null=True)

    distant_metastasis_stage = models.IntegerField(
        verbose_name='AJCC distant metastasis stage',
        choices=METASTASIS_STAGES,
        blank=True,
        null=True)

    cancer_therapy = models.CharField(
        verbose_name='Has patient received cancer-specific therapy?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    treatment_intent = models.CharField(
        verbose_name='Intent of cancer treatment',
        choices=TREATMENT_INTENT,
        max_length=10,
        blank=True,
        null=True)

    therapeutic_surgery = models.CharField(
        verbose_name='Has patient received therapeutic surgery?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    surgery_date = models.DateField(
        verbose_name='If yes, date of surgery',
        blank=True,
        null=True)

    surgery_date_estimated = models.CharField(
        verbose_name='Is the surgery date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    surgery_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    chemotherapy = models.CharField(
        verbose_name='Has patient received chemotherapy?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    chemotherapy_date = models.DateField(
        verbose_name='If yes, date of chemotherapy',
        blank=True,
        null=True)

    chemotherapy_date_estimated = models.CharField(
        verbose_name='Is the chemotherapy date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    chemotherapy_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    radiation = models.CharField(
        verbose_name='Has patient received radiation?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    radiation_date = models.DateField(
        verbose_name='If yes, date of radiation',
        blank=True,
        null=True)

    radiation_date_estimated = models.CharField(
        verbose_name='Is the radiation date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,)

    radiation_date_estimation = models.CharField(
        verbose_name='Which part of the date is estimated?',
        choices=DATE_ESTIMATION,
        max_length=15,
        null=True,
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = ('Cancer Diagnosis And Treatment Assessment '
                        '- Endpoint Recording')
        verbose_name_plural = ('Cancer Diagnosis And Treatment Assessments '
                               '- Endpoint Recordings')
