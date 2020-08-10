from .model_mixins import CrfModelMixin


class SymptomAndcareSeekingAssessment(CrfModelMixin):
    pass

    class Meta(CrfModelMixin.Meta):
        app_label = 'potlako_subject'
        verbose_name = 'Symptom And Care Seeking Assessment'
