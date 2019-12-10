from edc_constants.constants import ALIVE, DEAD, OTHER, POS, NEG, UNKNOWN, NOT_APPLICABLE

from .constants import DOCTOR_OTHER, MISSING, NURSE_OTHER

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

FACILITY_UNIT = (
    ('OPD', 'OPD'),
    ('A&E', 'A&E'),
    ('IDCC', 'IDCC'),
    ('medicine_ward', 'Medicine ward'),
    ('GYN_ward', 'GYN ward'),
    ('surgery_ward', 'Surgery ward'),
    (OTHER, 'Other'),
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

KIN_RELATIONSHIP = (
    ('spouse', 'Spouse'),
    ('child', 'Child'),
    ('parent', 'Parent'),
    ('sibling', 'Sibling'),
    ('grandparents', 'Grandparents'),
    ('grandchild', 'Grandchild'),
    (OTHER, 'Other')
)

SEVERITY_LEVEL = (
    ('low', 'Low'),
    ('moderate', 'Moderate'),
    ('high', 'High')
)

POS_NEG_UNKNOWN_MISSING = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (UNKNOWN, 'Unknown'),
    (MISSING, 'Missing'),
)

DISPOSITION = (
    ('return', 'Return'),
    ('refer', 'Refer'),
    ('discharge', 'Discharge'),
)

TRIAGE_STATUS = (
    ('emergency', 'Emergency'),
    ('urgent', 'Urgent'),
    ('routine', 'Routine'),
)

HOUSEMATE = (
    ('parents', 'Parents'),
    ('siblings', 'Siblings'),
    ('children', 'Children'),
    (OTHER, 'Other friend or relative'),
)

POS_NEG_MISSING_UNKNOWN = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    ('MISSING', 'Missing'),
    (UNKNOWN, 'Unknown'),
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

BUS_VOUCHER_STATUS = (
    ('not_drafted', 'Letter not yet drafted'),
    ('not_sent', 'Letter completed but not yet sent to facility'),
    ('not_received', 'Letter sent to facility (but not yet received)'),
    ('patient_received', 'Letter received by patient'),
    (OTHER, 'Other (specify)'),
    (NOT_APPLICABLE, 'N/A'),
)

CASH_TRANSFER_STATUS = (
    ('not_initiated', 'Transaction not yet initiated'),
    ('successful_confirmed', 'Transaction successful and patient confirmed'),
    ('successful_unconfirmed', 'Transaction successful but no patient confirmation'),
    ('not_successful', 'Transaction not successful (specify)'),
    (NOT_APPLICABLE, 'N/A'),
)

VISIT_TYPE = (
    ('referral', 'Referral'),
    ('return', 'Return'),
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

PEOPLE_INQUIRED_FROM = (
    ('patient_called', 'Patient called (phone answered)'),
    ('kin1_called',
     'Next of kin 1 called (phone answered) after patient called (NO answer, SMS sent)'),
    ('kin2_called', 'Next of kin 2 called (phone answered) after patient and next of '
                    'kin 1 called (NO answer for both, SMS sent to both)'),
    ('unreachable', 'Unable to reach patient or next of kin'),
)

REASON_MISSED_VISIT = (
    ('no_appointment_knowledge', 'Did not know about appointment'),
    ('forgot_appointment', 'Did not remember appointment date'),
    ('no_transport_fare', 'Could not afford transport fee'),
    ('no_access_to_transport', 'Did not have access to transportation'),
    ('different_facility', 'Went to a different facility'),
    ('felt_better', 'Did not think they had to come in because feeling better'),
    ('didnt_think_theyd_get_help',
     'Did not wish to return because they did not think they would get help'),
    ('deceased', 'Patient deceased'),
    (OTHER, 'Other (specify)'),
)

ALIVE_DEAD_LTFU = (
    (ALIVE, 'Patient alive (specify)'),
    (DEAD, 'Patient died'),
    ('ltfu', 'Patient lost to follow up')
)
