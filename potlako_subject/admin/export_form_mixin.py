class ExportCrfMixin:

    def export_crf_as_csv(self, request, queryset):
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        all_model_fields = ['field_name', 'field_type', 'verbose_name', 'choices']
        writer.writerow(all_model_fields)

        model_fields = meta.get_fields()

        for field in model_fields:
            field_list = []
            field_attributes = [field.name, field.get_internal_type(),
                                field.verbose_name, field.choices]

            for attribute in field_attributes:
                try:
                    print(attribute)
                except AttributeError:
                    field_list.append('')
                else:
                    field_list.append(attribute)

            writer.writerow(field_list)
        return response

    export_crf_as_csv.short_description = "Export model fields with description"
