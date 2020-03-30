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
    'potlako_subject.facility': [
        ('chobe', 'Chobe - Chobe'),
        ('bobonong', 'Central - Bobonong'),
        ('boteti', 'Central - Boteti'),
        ('mahalapye', 'Central - Mahalapye'),
        ('orapa', 'Central - Orapa'),
        ('serowe_palapye', 'Central - Serowe/Palapye'),
        ('tutume', 'Central - Tutume'),
        ('CKGR', 'ghanzi - CKGR'),
        ('ghanzi', 'ghanzi - Ghanzi'),
        ('kgalagdi_north', 'Kgalagadi North'),
        ('kgalagadi_south', 'Kgalagadi South'),
        ('kgatleng', 'Kgatleng'),
        ('kweneng_east', 'Kweneng - East'),
        ('kweneng_west', 'Kweneng - West'),
        ('delta', 'north West - Delta'),
        ('ngamiland_north', 'North West - Ngamiland Nort'),
        ('ngamiland_south', 'North East - Ngamiland South'),
        ('north_east', 'North East'),
        ('barolong', 'Southern - Barolong'),
        ('ngwaketse', 'Southern - Ngwaketse'),
        ('ngwaketse_west', 'Southern - Ngwaketse West'),
        (OTHER, 'Other (specify)')
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
    'potlako_subject.testtype': [
        ('blood_test', 'Blood test'),
        ('biopsy', 'Biopsy (specify body part)'),
        ('chest_xray', 'Chest X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct', 'CT'),
        (OTHER, 'Other')
    ]
}

preload_data = PreloadData(
    list_data=list_data)
