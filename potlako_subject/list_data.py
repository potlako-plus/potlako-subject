from edc_constants.constants import OTHER
from edc_list_data import PreloadData

list_data = {
    'potlako_subject.disposition': [
        ('return', 'Return'),
        ('refer', 'Refer'),
        ('discharge', 'Discharge')
    ],
    'potlako_subject.callachievements': [
        ('communicate_results', 'Communicate results'),
        ('reschedule_change_appointment', 'Reschedule/change appointment'),
        ('confirm_appointment_date', 'Confirm appointment date'),
        ('arrange_transportation', 'Arrange transportation'),
        (OTHER, 'Other')
    ],
    'potlako_subject.symptoms': [
        ('pain', 'Pain'),
        ('mass', 'Mass'),
        ('bleeding', 'Bleeding'),
        ('weight_loss', 'Weight loss'),
        ('dysphagia', 'Dysphagia'),
        ('dysuria', 'Dysuria'),
        (OTHER, 'Other (specify)')
    ],
}

preload_data = PreloadData(
    list_data=list_data)
