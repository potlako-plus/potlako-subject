from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, YES, NO, ON_STUDY 
from edc_constants.constants import PARTICIPANT, NEG, NOT_APPLICABLE
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import ClinicianCallEnrollment, PatientCallInitial 
from .models import SubjectConsent, SubjectScreening, SubjectVisit, SubjectLocator
from .models import MissedVisit, MissedCall, MissedCallRecord, PatientCallFollowUp
from .models import SymptomAndCareSeekingAssessment, CancerDxAndTx
from .models import HomeVisit, NextOfKin, InvestigationsOrdered, LabTest
from .models import PreviousFacilityVisit, FacilityVisit, InvestigationsResulted
from .models import BaselineClinicalSummary, BaselineRoadMap
from .models import CancerDxAndTxEndpoint, MedicalConditions, MedicalDiagnosis
from .models import EvaluationTimeline, NavigationSummaryAndPlan, SMS
from .models import SymptomAssessment, SymptomsAndCareSeekingEndpoint
from .models import Transport, VerbalConsent


fake = Faker()

cliniciancallenrollment = Recipe(
    ClinicianCallEnrollment,
    report_datetime=get_utcnow(),
    reg_date=get_utcnow().date(),
    contact_date=(get_utcnow() - relativedelta(months=1)).date(),
    cancer_suspect='call_with_clinician',
    cancer_suspect_other='blah',
    received_training = YES,
    call_clinician_type='nurse',
    consented_contact=YES,
    paper_register=YES,
    facility='nata_clinic',
    facility_other='blah',
    facility_unit='OPD',
    national_identity=seq('389221218'),
    first_name=fake.first_name,
    last_name=fake.last_name,
    age_in_years=35,
    gender='F',
    patient_contact=YES,
    primary_cell=seq('77654318'),
    village_town='nata',
    kin_details_provided=NO,
    clinician_type='med_officer',
    early_symptoms_date=(get_utcnow() - relativedelta(months=1)).date(),
    early_symptoms_date_estimated=NO,
    suspected_cancer='head_neck',
    suspicion_level='low',
    performance=0,
    pain_score='0_no_pain',
    last_hiv_result=NEG,
    patient_disposition='return',
    referral_date=(get_utcnow() + relativedelta(months=1)).date(),
    referral_unit=NOT_APPLICABLE,
    referral_discussed=NOT_APPLICABLE,
    triage_status='routine',
    investigated=NO 
)

nextofkin = Recipe(
    NextOfKin,
    kin_lastname='Test',
    kin_firstname='Test',
    kin_relationship='sibling',
    kin_relation_other='blah',
    kin_cell=seq('77123456'),
    kin_telephone=seq('3981218'),
)

subjectscreening = Recipe(
    SubjectScreening,
    has_diagnosis=YES,
    enrollment_interest=YES,
    residency=YES,
    nationality=YES,
    age_in_years=35,
    enrollment_site='molapowabojang_clinic',
)

subjectconsent = Recipe(
    SubjectConsent,
    subject_identifier=None,
    consent_datetime=get_utcnow(),
    dob=(get_utcnow() - relativedelta(years=25)).date(),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    gender='F',
    language='en',
    identity_type='OMANG',
    is_dob_estimated=NO,
    citizen=YES,
    version='1',
    consent_reviewed=YES,
    assessment_score=YES,
    verbal_script=YES,
    study_questions=YES,
)

subjectlocator = Recipe(
    SubjectLocator,
    subject_identifier=None,
    date_signed=get_utcnow().date())

subjectvisit = Recipe(
    SubjectVisit,
    report_datetime=get_utcnow(),
    reason=SCHEDULED,
    study_status=ON_STUDY,
    survival_status=ALIVE,
    info_source=PARTICIPANT)

patientcallinitial = Recipe(
    PatientCallInitial,
    patient_call_date=get_utcnow().date(),
    patient_call_time=get_utcnow().time(),
    hiv_test_date=get_utcnow().date(),
    age_in_years=25,
    education_level='secondary',
    work_status='no',
    transport_support=NO,
    medical_conditions=NO,
    tests_ordered=NO,
    heard_of_potlako=YES
)

previousfacilityvisit = Recipe(
    PreviousFacilityVisit,
    facility_visited='athlone_hospital',
    facility_visited_other='blah',
    previous_facility_period='2 weeks'
)

baselineclinicalsummary = Recipe(
    BaselineClinicalSummary,)

baselineroadmap = Recipe(
    BaselineRoadMap,
    investigations_turnaround_time=(get_utcnow() + relativedelta(days=5)).date(),
    review_turnaround_time=(get_utcnow() + relativedelta(days=5)).date(),
    oncology_visit=(get_utcnow() + relativedelta(days=5)).date(),
    oncology_turnaround_time=(get_utcnow() + relativedelta(days=5)).date(),
    treatment_initiation_visit=(get_utcnow() + relativedelta(days=5)).date(),
    treatment_initiation_turnaround_time=(get_utcnow() + relativedelta(days=5)).date())

cancerdxAndtxendpoint = Recipe(
    CancerDxAndTxEndpoint,)

medicalconditions = Recipe(
    MedicalConditions,)

medicaldiagnosis = Recipe(
    MedicalDiagnosis,)

evaluationtimeline = Recipe(
    EvaluationTimeline,)


navigationsummaryandplan = Recipe(
    NavigationSummaryAndPlan,)

sms = Recipe(
    SMS,)

symptomandcareseekingassessment = Recipe(
    SymptomAndCareSeekingAssessment,
    clinic_visit_date=get_utcnow().date())

patientcallfollowup = Recipe(
    PatientCallFollowUp,
    encounter_date=get_utcnow().date(),
    start_time=get_utcnow().time(),
    investigations_ordered='blah',
    last_visit_date=get_utcnow() - relativedelta(days=1),
    next_appointment_date=get_utcnow() + relativedelta(months=2)
)

facilityvisit = Recipe(
    FacilityVisit,
    interval_visit_date=get_utcnow().date(),
    interval_visit_date_estimated='No',
    visit_facility='otse_clinic',
    visit_outcome='return')

cancerdxandtx = Recipe(
    CancerDxAndTx,)

investigationsordered = Recipe(
    InvestigationsOrdered,
    ordered_date=get_utcnow().date(),)

labtest = Recipe(
    LabTest,
    lab_test_type='FBC',
    lab_test_date=get_utcnow().date(),
    lab_test_status='results_available_paper',)

investigationsresulted = Recipe(
    InvestigationsResulted,
    diagnosis_results='inconclusive',)

homevisit = Recipe(
    HomeVisit,
    next_appointment=(get_utcnow() + relativedelta(months=1)).date())

missedvisit = Recipe(
    MissedVisit,)

missedcall = Recipe(
    MissedCall,)

missedcallrecord = Recipe(
    MissedCallRecord,)

symptomassessment = Recipe(
    SymptomAssessment,)

symptomsandcareseekingendpoint = Recipe(
    SymptomsAndCareSeekingEndpoint,)

transport = Recipe(
    Transport,)

verbalconsent = Recipe(
    VerbalConsent,)
