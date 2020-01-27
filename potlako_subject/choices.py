from edc_constants.constants import (
    ALIVE, DEAD, OTHER, POS, NEG, OFF_STUDY, UNKNOWN, NOT_APPLICABLE, NONE)

from .constants import DOCTOR_OTHER, MISSING, NURSE_OTHER

ALIVE_DEAD_LTFU = (
    (ALIVE, 'Patient alive (specify)'),
    (DEAD, 'Patient died'),
    ('ltfu', 'Patient lost to follow up')
)

BUS_VOUCHER_STATUS = (
    ('not_drafted', 'Letter not yet drafted'),
    ('not_sent', 'Letter completed but not yet sent to facility'),
    ('not_received', 'Letter sent to facility (but not yet received)'),
    ('patient_received', 'Letter received by patient'),
    (OTHER, 'Other (specify)'),
    (NOT_APPLICABLE, 'N/A'),
)

CANCER_DIAGNOSIS = (
    ('cervical', 'Cervical Cancer'),
    ('breast', 'Breast Cancer'),
    ('head_n_neck', 'Head and Neck Cancer'),
    ('non_hodgkin_lymph', 'Non-Hodgkin Lymphoma'),
    ('hodgkin_lymph', 'Hodgkin Lymphoma'),
    ('esophageal', 'Esophageal'),
    ('vuginal', 'Vulvar/Vaginal Cancer'),
    ('anal', 'Anal Cancer'),
    ('kaposis_sarcoma', 'Kaposi\'s sarcoma'),
    ('penile', 'Penile Cancer'),
    ('prostate', 'Prostate Cancer'),
    ('colorectal', 'Colorectal Cancer'),
    (OTHER, 'Other'),
)

CANCER_EVALUATION = (
    ('complete', 'Complete'),
    ('unable_to_complete',
     'Incomplete, but unable to complete (i.e. death, refusal)'),
    ('incomplete_needs_priority',
     'Incomplete, needs priority Potlako follow-up'),
    ('complete_needs_priority', 'Complete, needs priority Potlako follow-up')
)

CANCER_STAGES = (
    ('stage_0', 'Stage 0'),
    ('stage_I', 'Stage I'),
    ('stage_II', 'Stage II'),
    ('stage_III', 'Stage III'),
    ('stage_IV', 'Stage IV'),
    (OTHER, 'Other'),
)

CANCER_STATUS = (
    ('confirmed', 'Confirmed cancer'),
    ('probable', 'Probable cancer'),
    ('possible_not', 'Possible not cancer'),
    ('probable_not', 'Probable not cancer, no alternative dx'),
    ('confirmed_not', 'Confirmed not cancer, alternative dx'),
    ('incomplete_dx', 'Incomplete dx'),
)

CASH_TRANSFER_STATUS = (
    ('not_initiated', 'Transaction not yet initiated'),
    ('successful_confirmed', 'Transaction successful and patient confirmed'),
    ('successful_unconfirmed', 'Transaction successful but no patient '
     'confirmation'),
    ('not_successful', 'Transaction not successful (specify)'),
    (NOT_APPLICABLE, 'N/A'),
)

CLINICIAN_TYPE = (
    ('med_officer', 'Medical Officer'),
    ('fam_medicine', 'Specialist - Family Medicine'),
    ('internal_medicine', 'Specialist - Internal Medicine'),
    ('general_surgeon', 'Specialist - General Surgeon'),
    ('ob_gyn', 'Specialist - Ob/GYN (Gynecologist)'),
    ('oncologist', 'Specialist - Oncologist'),
    ('pathologist', 'Specialist - Pathologist'),
    ('hematologist', 'Specialist - Hematologist'),
    ('palliative_care', 'Specialist - Palliative care'),
    (DOCTOR_OTHER, 'Doctor - Other type (specify)'),
    ('FNP', 'Nurse - FNP'),
    ('midwife', 'Nurse - Midwife'),
    ('community_health', 'Nurse - Community health'),
    (NURSE_OTHER, 'Nurse - Other type (specify)'),
    ('RN', 'Nurse - RN')
)

COMPONENTS_RECEIVED = (
    ('provider_edication', 'Provider education'),
    ('diagnostic_facilitation', 'Diagnostic facilitation (pre-biopsy/test)'),
    ('access_to_diagnostic_results',
     'Access to diagnostic results (e.g. histology)'),
    ('cancer_treatment_facilitation_post_test_results',
     'Cancer treatment facilitation post-test results'),
    ('retention_or_completion_of_cancer_treatment',
     'Retention or completion of cancer treatment'),
    (NONE, 'None'),
    (OTHER, 'Other (specify)'),
)

DEATH_INFO_SOURCE = (
    ('clinician', 'Clinician'),
    ('next_of_kin1', 'Next of kin 1'),
    ('next_of_kin2', 'Next of kin 2'),
    ('other_fam_member', 'Other family member'),
    (OTHER, 'Other (specify)'),
)

DETERMINE_MISSED_VISIT = (
    ('database',
     'Coordinator referenced database and contacted clinician/facility'),
    ('clinic_register',
     'Clinician referenced clinic register and contacted clinician'),
    ('clinician_contacted', 'Patient contacted clinician'),
    ('coordinator_contacted', 'Patient contacted coordinator'),
    (OTHER, 'Other')
)

DELAYED_REASON = (
    ('patient_factor', 'Patient Factor'),
    ('health_system_factor', 'Health System Factor')
)

DIAGNOSIS_RESULTS = (
    ('not_cancer', 'NOT cancer'),
    ('cancer', 'cancer'),
    ('non_diagnostic', 'Non-diagnostic'),
    ('specimen_not_recieved', 'Specimen lost or not received')
)

DISPOSITION = (
    ('return', 'Return'),
    ('refer', 'Refer'),
    ('discharge', 'Discharge'),
)

DISTRICT = (
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
)

FACILITY = (
    ('boatlaname_hp', 'Boatlaname HP'),
    ('bokaa_pc', 'Bokaa PC'),
    ('borakalalo_pc', 'Borakalalo PC'),
    ('boribamo_pc', 'Boribamo PC'),
    ('boswelakoko_pc', 'Boswelakoko PC'),
    ('ditshukudu_hp', 'Ditshukudu HP'),
    ('gakgatla_hp', 'Gakgatla HP'),
    ('gakuto_hp', 'Gakuto HP'),
    ('gamodubu_hp', 'Gamodubu HP'),
    ('hatsalatladi_hp', 'Hatsalatladi HP'),
    ('kgope_hp', 'Kgope HP'),
    ('kgosing_pc', 'Kgosing PC'),
    ('kopong_pc', 'Kopong PC'),
    ('kubung_hp', 'Kubung HP'),
    ('kumakwane_hp', 'Kumakwane HP'),
    ('kweneng_hp', 'Kweneng HP'),
    ('lekgwapheng_hp', 'Lekgwapheng HP'),
    ('lentsweletau_pc', 'Lentsweletau PC'),
    ('lephepe_pc', 'Lephepe PC'),
    ('lesilakgokong_hp', 'Lesilakgokong HP'),
    ('loologane_pc', 'Loologane PC'),
    ('magokotswane_hp', 'Magokotswane HP'),
    ('mahetlwe_hp', 'Mahetlwe HP'),
    ('medie_hp', 'Medie HP'),
    ('mmankgodi_pc', 'Mmankgodi PC'),
    ('mmanoko_hp', 'Mmanoko HP'),
    ('mmatseta_hp', 'Mmatseta HP'),
    ('mogonono_hp', 'Mogonono HP'),
    ('molepolole_comm_clinic_pc', 'Molepolole Community Clinic PC'),
    ('phuthadikobo_pc', 'Phuthadikobo PC'),
    ('phuting_hp', 'Phuting HP'),
    ('rungwane_hp', 'Rungwane HP'),
    ('shadishadi_hp', 'Shadishadi HP'),
    ('SLH', 'SLH - Scotting Livingstone Hospital'),
    ('sojwe_pc', 'Sojwe PC'),
    ('thamaga_pc', 'Thamaga PC'),
    ('TPH', 'TPH - Thamaga PH'),
    ('marotse_ms', 'Marotse MS'),
    ('chaoke_ms', 'Chaoke MS'),
    ('dam18_ms', 'Dam 18 MS'),
    ('dikgathong_ms', 'Dikgathong MS'),
    ('dikhutsana_ms', 'Dikhutsana MS'),
    ('diphepe_ms', 'Diphepe MS'),
    ('gamatsela_ms', 'Gamatsela MS'),
    ('gamononyane_ms', 'Gamononyane MS'),
    ('hubasanoko_ms', 'Hubasanoko MS'),
    ('kaminakwe_ms', 'Kaminakwe MS'),
    ('kgapamadi_ms', 'Kgapamadi MS'),
    ('khuduyamajako_ms', 'Khuduyamajako MS'),
    ('kokonje_ms', 'Kokonje MS'),
    ('lekgatshwane_ms', 'Lekgatshwane MS'),
    ('maanege_ms', 'Maanege MS'),
    ('mapateng_ms', 'Mapateng MS'),
    ('mmakanke_ms', 'Mmakanke MS'),
    ('mmamarobole_ms', 'Mmamarobole MS'),
    ('mmamohiko_ms', 'Mmamohiko MS'),
    ('mmankgodi_east_ms', 'Mmankgodi East MS'),
    ('mmaothate_ms', 'Mmaothate MS'),
    ('mmapaba_ms', 'Mmapaba MS'),
    ('mmasebele_ms', 'Mmasebele MS'),
    ('moamoge_ms', 'Moamoge MS'),
    ('moetlo_ms', 'Moetlo MS'),
    ('mophakane_ms', 'Mophakane MS'),
    ('mosekele_ms', 'MoseKELE MS'),
    ('moselele1_ms', 'Moselele 1 MS'),
    ('moselele2_ms', 'Moselele 2 MS'),
    ('mosokotso_ms', 'Mosokotso MS'),
    ('motlabaki_ms', 'Motlabaki MS'),
    ('phiriyabokwetse_ms', 'Phiriyabokwetse MS'),
    ('ramagapu_ms', 'Ramagapu MS'),
    ('ramakgatlanyane_ms', 'Ramakgatlanyane MS'),
    ('ramankhung_ms', 'Ramankhung MS'),
    ('ramaphatle_ms', 'Ramankhung MS'),
    ('ramasenyane_ms', 'Ramasenyane MS'),
    ('rammidi_ms', 'Rammidi MS'),
    ('rasegwagwa_ms', 'Rammidi MS'),
    ('sasakwe_ms', 'Sasakwe MS'),
    ('sekhukhwane_ms', 'Sekhukhwane MS'),
    ('sepene_ms', 'Sepene MS'),
    ('shonono_ms', 'Shonono MS'),
    ('suping_ms', 'Suping MS'),
    ('scatter&lamber_pc', 'Scatter & Lamber PC (private)'),
    ('ikago_pc', 'Ikago PC'),
    ('mec_pc', 'Molepopole Education Centre PC'),
    ('molepolole_prisons_pc', 'Molepolole Prisons PC'),
    ('princess_marina', 'Princess Marina Hospital'),
)

FACILITY_TYPE = (
    ('health_post', 'health post'),
    ('primary_clinic', 'primary clinic'),
    ('primary_hospital', 'primary hospital'),
    ('secondary_hospital', 'secondary hospital'),
    ('referral_hospital', 'referral hospital')
)

FACILITY_UNIT = (
    ('OPD', 'OPD'),
    ('A&E', 'A&E'),
    ('IDCC', 'IDCC'),
    ('medicine_ward', 'Medicine ward'),
    ('GYN_ward', 'GYN ward'),
    ('surgery_ward', 'Surgery ward'),
    (OTHER, 'Other'),
)

HEALTH_FACTOR = (
    ('clinic_hospital_unable_schedule_2_weeks', 'Clinic/hospital unable to '
     'schedule within 2 weeks (overbooked, uncertain schedule, etc)'),
    ('clinic_hospital_did_not_schedule_2_weeks', 'Clinic/hospital did not '
     'schedule within 2 weeks (unwilling, low priority case, etc)'),
    ('clinic_no_transport', 'Clinic/hospital provided transportation not '
     'available (needed for other clinic use, broken, driver on leave, etc)'),
    ('service_unavailable',
     'Clinic/hospital service no available on scheduled date (surgical '
     'consultation, biopsy clinic, etc)'),
    ('service_provider_not_available',
     'Clinic/hospital provider not  available on scheduled date (provider '
     'called to emergency, provider on leave, etc)'),
    ('supplies_not_available', 'Clinic/hospital supplies not available on '
     'scheduled date (no biopsy needles, out of stock chemotherapy, etc)'),
    (OTHER, 'other clinic or hospital related reason (specify)')
)

HOUSEMATE = (
    ('parents', 'Parents'),
    ('siblings', 'Siblings'),
    ('children', 'Children'),
    (OTHER, 'Other friend or relative'),
)

IMAGING_STATUS = (
    ('ordered', 'Ordered'),
    ('performed', 'Performed')
)

IMAGING_TESTS = (
    ('xray_chest', 'Xray - chest'),
    ('xray_other', 'Xray - other (specify)'),
    ('ultrasound_abdomen', 'Ultrasound - abdomen'),
    ('ultrasound_other', 'Ultrasound - other (specify)'),
    ('CT', 'CT (specify)'),
    ('MRI', 'MRI (specify)'),
    (OTHER, 'Other imaging test (specify)')
)

KIN_RELATIONSHIP = (
    ('spouse', 'Spouse'),
    ('child', 'Child'),
    ('parent', 'Parent'),
    ('sibling', 'Sibling'),
    ('grandparents', 'Grandparents'),
    ('grandchild', 'Grandchild'),
    (OTHER, 'Other')
)

LAB_TESTS = (
    ('FBC', 'FBC'),
    ('RFT', 'RFT'),
    ('LFT', 'LFT'),
    ('HIV', 'HIV'),
    ('WBC', 'WBC'),
    ('Hb', 'Hb'),
    ('Plt', 'Plt'),
    ('Cr', 'Cr'),
    ('K', 'K'),
    ('Na', 'Na'),
    ('Glu', 'Glu'),
    ('pap_smear', 'Pap Smear'),
    (OTHER, 'Other lab test (specify)')
)

LAB_TESTS_STATUS = (
    ('ordered', 'Ordered'),
    ('specimen_taken', 'Specimen taken'),
    ('specimen_logged_ipms', 'Specimen logged into IPMS'),
    ('specimen_recieved_nhl', 'Specimen received at NHL (for pathology only)'),
    ('results_available_ipms', 'Results available on IPMS'),
    ('results_available_paper', 'Results available on paper'),
    (OTHER, 'Other (specify)')
)

LTFU_CRITERIA = (
    ('missed_visits', 'Missed visits'),
    ('attempted_calls_to_patient',
     'attempted calls to patient x 3 or 3 different days'),
    ('attempted_calls_to_next_kin1',
     'attempted calls to next of kin 1 x 3 or 3 different days'),
    ('attempted_calls_to_next_kin2',
     'attempted calls to next of kin 2 x 3 or 3 different days'),
    ('home_visit_done_unable_to_trace', 'home visit done and unable to trace'),
)

NON_CANCER_DIAGNOSIS = (
    ('fibroadenoma', 'Fibroadenoma'),
    ('breast_cyst', 'Breast cyst'),
    ('breast_abscess', 'Breast Abscess'),
    ('tb', 'Tuberculosis'),
    ('skin_ulcer', 'Non-healing skin ulcer'),
    ('pre_cancerous_lesion', 'Cervical pre-cancerous lesion'),
    ('no_alt_diagnosis_est', 'No alternative diagnosis established'),
    (OTHER, 'Other'),
)

PATIENT_FACTOR = (
    ('patient_work_obligations', 'Patient work obligations (formal '
     'and informal work, including lands and cattle post)'),
    ('patient_family_obligations', 'Patient family obligations '
     '(childcare, funeral, illness in family, etc)'),
    ('patient_paying_transport_difficulty', 'Patient difficulty paying for '
     'transportation, including family member to accompany'),
    ('patient_finding_tarnsport_difficulty', 'Patient difficulty finding '
     'transportation or family member to accompany'),
    (OTHER, 'Other patient related reason (specify)')
)

PEOPLE_INQUIRED_FROM = (
    ('patient_called', 'Patient called (phone answered)'),
    ('kin1_called',
     'Next of kin 1 called (phone answered) after patient called (NO answer, '
     'SMS sent)'),
    ('kin2_called', 'Next of kin 2 called (phone answered) after patient and '
     'next of kin 1 called (NO answer for both, SMS sent to both)'),
    ('unreachable', 'Unable to reach patient or next of kin'),
)

PLACE_OF_DEATH = (
    ('home', 'At home or in the community'),
    ('facility', 'At facility'),
    (UNKNOWN, 'Place of death unknown'),
)

POS_NEG_UNKNOWN_MISSING = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (UNKNOWN, 'Unknown'),
    (MISSING, 'Missing'),
)

PATHOLOGY_TEST_TYPE = (
    ('biopsy_bone_marrow', 'Biopsy - bone marrow'),
    ('biopsy_lymph_node', 'Biopsy - lymph node'),
    ('biopsy_other', 'Biopsy - other (specify)'),
    ('FNA', 'FNA'),
    ('pap_smear', 'Pap smear')
)

REASON_FOR_EXIT = (
    ('death', 'Patient death'),
    ('ltfu', 'Patient lost to follow-up'),
    ('eval_complete', 'Cancer evaluation complete'),
    ('declines_further_eval',
     'Patient or clinician declines further evaluation'),
    ('patient_requests_removal', 'Patient requests removal from Potlako'),
    ('clinician_requests_removal', 'Clinician requests removal from Potlako'),
)

REASON_MISSED_VISIT = (
    ('no_appointment_knowledge', 'Did not know about appointment'),
    ('forgot_appointment', 'Did not remember appointment date'),
    ('no_transport_fare', 'Could not afford transport fee'),
    ('no_access_to_transport', 'Did not have access to transportation'),
    ('different_facility', 'Went to a different facility'),
    ('felt_better',
     'Did not think they had to come in because feeling better'),
    ('didnt_think_theyd_get_help',
     'Did not wish to return because they did not think they would get help'),
    ('deceased', 'Patient deceased'),
    (OTHER, 'Other (specify)'),
)

REVIEWER = (
    ('neo', 'Neo'),
    ('scott', 'Scott'),
    (OTHER, 'Other')
)

SEVERITY_LEVEL = (
    ('low', 'Low'),
    ('moderate', 'Moderate'),
    ('high', 'High')
)

SMS_OUTCOME = (
    ('patient_sent_sms_received', 'SMS sent to patient and receipt confirmed'),
    ('patient_sent_sms_not_received', 'SMS sent to patient and receipt NOT '
     'confirmed'),
    ('kin1_sent_sms_received', 'SMS sent to next of kin 1 and receipt '
     'confirmed'),
    ('kin1_sent_sms_not_received',
     'SMS sent to next of kin 1 and receipt NOT confirmed'),
    ('kin2_sent_sms_received', 'SMS sent to next of kin 2 and receipt '
     'confirmed'),
    ('kin2_sent_sms_not_received',
     'SMS sent to next of kin 2 and receipt NOT confirmed'),
)

TEST_TYPE = (
    ('blood_test', 'Blood test'),
    ('biopsy', 'Biopsy (specify body part)'),
    ('chest_xray', 'Chest X-Ray'),
    ('ultrasound', 'Ultrasound'),
    ('ct', 'CT'),
    (OTHER, 'Other')
)

TRANSPORT_CRITERIA = (
    ('social_welfare_assistance', 'On social welfare assistance'),
    ('disability', 'Unable to work due to physical or mental disability'),
    ('residing_in_mobile_stop_area', 'Residing in mobile stop area'),
    ('no_public_transport', 'Residing in area with no public transport'),
    ('lives_far', 'Lives >= 20km away from nearest health facility'),
    ('missed_visits_due_trans_challenges',
     'Has missed appointments due to transportation challenges'),
    (OTHER, 'Other'),
)

TRANSPORT_TYPE = (
    ('facility_vehicle', 'Facility Vehicle - Arranged by RC'),
    ('bus', 'Bus Voucher'),
    ('cash', 'Cash transfer to patient'),
    ('patient_arranged_vehicle',
     'Facility Vehicle - Arranged by Patient or Clinician'),
)

TREATMENT_INTENT = (
    ('curative', 'Curative'),
    ('palliative', 'Palliative'),
    ('uncertain', 'Uncertain'),
)

TRIAGE_STATUS = (
    ('emergency', 'Emergency'),
    ('urgent', 'Urgent'),
    ('routine', 'Routine'),
)

VEHICLE_ARR_STATUS = (
    ('in_progress', 'Request made to facility, arrangement in progress'),
    ('to_be_communicated',
     'Arrangement confirmed by facility but not yet communicated with '
     'patient or clinician'),
    ('confirmed_communicated',
     'Arrangement confirmed by facility and communicated to the patient '
     'and clinician'),
    ('vehicle_cannot_be_provided', 'Request made facility NOT able to '
     'provide transport/vehicle for patient'),
    (OTHER, 'Other (specify)'),
    (NOT_APPLICABLE, 'N/A'),
)

VISIT_TYPE = (
    ('referral', 'Referral'),
    ('return', 'Return'),
)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

VISIT_UNSCHEDULED_REASON_CHOICE = (
    ('Routine oncology clinic visit (i.e. planned chemo, follow-up)',
     'Routine oncology clinic visit (i.e. planned chemo, follow-up)'),
    ('Ill oncology clinic visit', 'Ill oncology clinic visit'),
    ('Patient called to come for visit', 'Patient called to come for visit'),
    ('Other, specify: ', 'Other, specify: '),
)

VISIT_UNSCHEDULED_REASON = (
    ('Routine oncology', 'Routine oncology clinic visit (i.e. planned chemo, follow-up)'),
    ('Ill oncology', 'Ill oncology clinic visit'),
    ('Patient called', 'Patient called to come for visit'),
    (NOT_APPLICABLE, 'Not Applicable'),
    ('OTHER', 'Other, specify:'),
)

VISIT_REASON = (
    ('Quarterly visit/contact', 'Quarterly visit/contact'),
    ('Unscheduled visit/contact', 'Unscheduled visit/contact'),
    ('Missed quarterly visit', 'Missed quarterly visit'),
    ('Lost to follow-up', 'Lost to follow-up (use only when taking subject off study)'),
    ('Death', 'Death'),
    (OFF_STUDY, 'Off study'),
    ('deferred', 'Deferred'),
)

VISIT_INFO_SOURCE = (
    ('Clinic visit w/ subject', 'Clinic visit with participant'),
    ('Other contact w/ subject', 'Other contact with participant (i.e telephone call)'),
    ('Contact w/ health worker', 'Contact with health care worker'),
    ('Contact w/ family/design',
     'Contact with family or designated person who can provide information'),
    ('OTHER', 'Other,specify'),
)