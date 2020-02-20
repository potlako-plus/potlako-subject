from edc_base.model_mixins import ListModelMixin, BaseUuidModel

from .model_mixins import ModelCsvFormExportMixin


class Disposition(ListModelMixin, BaseUuidModel):

    model_csv_form_export = ModelCsvFormExportMixin


class CallAchievements(ListModelMixin, BaseUuidModel):

    model_csv_form_export = ModelCsvFormExportMixin
