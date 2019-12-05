from edc_list_data import PreloadData


list_data = {
    'potlako_subject.disposition': [
        ('return', 'Return'),
        ('refer', 'Refer'),
        ('discharge', 'Discharge')
    ],
}

preload_data = PreloadData(
    list_data=list_data)
