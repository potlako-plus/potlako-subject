from .model_mixins import CrfModelMixin


class CancerDiagnosisAndTreatmentAssessment(CrfModelMixin):
    pass

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Cancer Diagnosis And Treatment Assessment'
