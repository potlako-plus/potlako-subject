from edc_base.model_mixins import ListModelMixin, BaseUuidModel


class Disposition(ListModelMixin, BaseUuidModel):
    pass


class CallAchievements(ListModelMixin, BaseUuidModel):
    pass


class Symptoms(ListModelMixin, BaseUuidModel):
    pass


class TestType(ListModelMixin, BaseUuidModel):
    pass
