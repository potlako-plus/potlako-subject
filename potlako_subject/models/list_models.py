from edc_base.model_mixins import ListModelMixin, BaseUuidModel


class DiscussionPerson(ListModelMixin, BaseUuidModel):
    pass


class Disposition(ListModelMixin, BaseUuidModel):
    pass


class CallAchievements(ListModelMixin, BaseUuidModel):
    pass


class Housemate(ListModelMixin, BaseUuidModel):
    pass


class ImagingTestType(ListModelMixin, BaseUuidModel):
    pass


class InvestigationNotes(ListModelMixin, BaseUuidModel):
    pass


class PatientResidence(ListModelMixin, BaseUuidModel):
    pass


class PathologyTest(ListModelMixin, BaseUuidModel):
    pass


class SmsPlatform(ListModelMixin, BaseUuidModel):
    pass

class SourceOfInfo(ListModelMixin, BaseUuidModel):
    pass


class Symptoms(ListModelMixin, BaseUuidModel):
    pass


class TestType(ListModelMixin, BaseUuidModel):
    pass


class TestsOrderedType(ListModelMixin, BaseUuidModel):
    pass


class TransportCriteria(ListModelMixin, BaseUuidModel):
    pass
