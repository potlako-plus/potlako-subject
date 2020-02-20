import csv


class ModelCsvFormExportMixin:

    def __init__(self, model=None):
        self.model = model
    
    @property
    def fields_verbose_names(self):
        """Return a list of list of field and verbose name.
        """
        exclude_list = [
            'created', 'id', 'device_created', 'device_modified',
            'modified', 'user_created', 'user_modified', 'hostname_created',
            'hostname_modified', 'revision']
        f_list= [[field.name, self.model._meta.get_field(field.name).verbose_name] for field in self.model._meta.fields if field.name not in exclude_list]
        header = [['Field name', 'Questionnaire']]
        field_list = header + f_list
        return field_list

    @property
    def export_from_as_csv(self):

        with open(self.model._meta.label_lower + '.csv', "w+") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.fields_verbose_names)