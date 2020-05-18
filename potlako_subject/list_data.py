from edc_constants.constants import OTHER
from edc_list_data import PreloadData

list_data = {
    'potlako_subject.disposition': [
        ('return', 'Return'),
        ('refer', 'Refer'),
        ('discharge', 'Discharge')
    ],
    'potlako_subject.housemate': [
        ('parents', 'Parents'),
        ('siblings', 'Siblings'),
        ('children', 'Children'),
        ('spouse', 'Spouse'),
        (OTHER, 'Other (specify)'),
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
        ('bowel_movements_change', 'Change in bowel movements'),
        ('discharge', 'Discharge'),
        ('weight_loss', 'Weight loss'),
        ('dysphagia', 'Dysphagia'),
        ('dysuria', 'Dysuria'),
        ('altered_bowel_movement', 'Altered Bowel Movement'),
        ('skin_changes', 'Skin changes'),
        (OTHER, 'Other (specify)')
    ],
    'potlako_subject.testtype': [
        ('blood_test', 'Blood test'),
        ('biopsy', 'Biopsy (specify body part)'),
        ('chest_xray', 'Chest X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct', 'CT'),
        (OTHER, 'Other')
    ],
    'potlako_subject.transportcriteria': [
        ('social_welfare_assistance', 'On social welfare assistance'),
        ('disability', 'Unable to work due to physical or mental disability'),
        ('residing_in_mobile_stop_area', 'Residing in mobile stop area'),
        ('no_public_transport', 'Residing in area with no public transport'),
        ('lives_far', 'Lives >= 20km away from nearest health facility'),
        ('missed_visits_due_trans_challenges',
         'Has missed appointments due to transportation challenges'),
        (OTHER, 'Other'),
    ]
}

preload_data = PreloadData(
    list_data=list_data)
