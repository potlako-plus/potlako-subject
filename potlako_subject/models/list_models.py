from edc_base.model_mixins import ListModelMixin, BaseUuidModel


class Disposition(ListModelMixin, BaseUuidModel):
    pass


class CallAchievements(ListModelMixin, BaseUuidModel):
    pass


class Housemate(ListModelMixin, BaseUuidModel):
    pass


class InvestigationNotes(ListModelMixin, BaseUuidModel):
    pass


class PatientResidence(ListModelMixin, BaseUuidModel):
    pass


class PathologyTestType(ListModelMixin, BaseUuidModel):
    pass


class Symptoms(ListModelMixin, BaseUuidModel):
    pass


class TestType(ListModelMixin, BaseUuidModel):
    pass


class TransportCriteria(ListModelMixin, BaseUuidModel):
    pass
