from edc_constants.constants import OTHER, NOT_APPLICABLE, NONE
from edc_list_data import PreloadData

list_data = {
    'potlako_subject.discussionperson': [
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('sister', 'Sister'),
        ('brother', 'Brother'),
        ('female_family_member', 'Other female family member'),
        ('male_family_member', 'Other male family member'),
        ('female_friend', 'Female friend'),
        ('male_friend', 'Male friend'),
        ('pastor_religious_leader', 'Pastor or religious leader'),
        ('traditional_healer', 'Traditional healer'),
        ('spouse', 'Spouse'),
        ('children', 'Children'),
        (OTHER, 'Other (specify)')
    ],
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
    'potlako_subject.imagingtesttype': [
        ('xray', 'Xray (specify)'),
        ('ultrasound', 'Ultrasound (specify)'),
        ('CT', 'CT (specify)'),
        ('MRI', 'MRI (specify)'),
        (OTHER, 'Other imaging test (specify)')
    ],
    'potlako_subject.investigationnotes': [
        ('LFTs', 'LFTs'),
        ('U&Es', 'U&Es'),
        ('ESR', 'ESR'),
        ('FBC', 'FBC'),
        ('CXR', 'CXR'),
        ('USS', 'USS'),
        ('U/A', 'U/A'),
        ('microscopy', 'Microscopy'),
        (NOT_APPLICABLE, 'Not applicable'),
        (OTHER, 'Other (specify)'),
    ],
    'potlako_subject.patientresidence': [
        ('alone', 'Alone'),
        ('spouse', 'Spouse'),
        ('parents', 'Parents'),
        ('siblings', 'Siblings'),
        ('children', 'Children'),
        ('live_in_partner', 'Live-in partner'),
        (OTHER, 'Other (specify)')
    ],
    'potlako_subject.pathologytest': [
        ('biopsy', 'Biopsy (specify)'),
        ('FNA', 'FNA'),
        ('pap_smear', 'Pap smear'),
        (OTHER, 'Other (specify)')
    ],
    'potlako_subject.sourceofinfo': [
        ('relative', 'Relative'),
        ('spouse', 'Spouse'),
        ('potlako_plus_member', 'Potlako+ team member'),
        ('health_care_worker', 'Health care worker'),
        (OTHER, 'Other (specify)')
    ],
    'potlako_subject.symptoms': [
        ('mouth_pain', 'Mouth pain'),
        ('pelvic_pain', 'Pelvic pain'),
        ('abdominal_pain', 'Abdominal pain'),
        ('new_mass_lump', 'New mass or lump'),
        ('bleeding', 'Bleeding'),
        ('bowel_movements_change', 'Change in bowel movements'),
        ('discharge', 'Discharge'),
        ('weight_loss', 'Weight loss'),
        ('dysphagia', 'Dysphagia'),
        ('dysuria', 'Dysuria'),
        ('skin_changes', 'Skin changes'),
        ('cough', 'Cough'),
        (NONE, 'None'),
        (OTHER, 'Other (specify)')
    ],
    'potlako_subject.testsorderedtype': [
        ('pathology', 'Pathology'),
        ('imaging', 'Imaging'),
        (OTHER, 'Other (specify)')
    ],
    'potlako_subject.transportcriteria': [
        ('social_welfare_assistance', 'On social welfare assistance'),
        ('disability', 'Unable to work due to physical or mental disability'),
        ('residing_in_mobile_stop_area', 'Residing in mobile stop area'),
        ('no_public_transport', 'Residing in area with no public transport'),
        ('lives_far', 'Lives >= 20km away from nearest health facility'),
        ('missed_visits_due_trans_challenges',
         'Has missed appointments due to transportation challenges'),
        (NONE, 'None of the above'),
        (OTHER, 'Other'),
    ],
    'potlako_subject.smsplatform': [
        ('potlako+_iec_material', 'Potlako+ IEC material'),
        ('group_teaching', 'Group teaching'),
        ('public_campaign', 'Public campaign'),
        ('info_from_community_leader', 'Information from community leader'),
        (OTHER, 'Other, specify'),
    ]
}

preload_data = PreloadData(
    list_data=list_data)
