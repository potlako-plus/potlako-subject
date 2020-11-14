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


fake = Faker()

cliniciancallenrollment = Recipe(
    ClinicianCallEnrollment,
    reg_date=get_utcnow(),
    contact_date=get_utcnow() - relativedelta(months=1),
    cancer_suspect='call_with_clinician',
    received_training = YES,
    call_clinician_type='nurse',
    consented_contact=YES,
    paper_register=YES,
    facility='molapowabojang_clinic',
    facility_unit='OPD',
    national_identity=seq('389201212'),
    first_name=fake.first_name,
    last_name=fake.last_name,
    age_in_years=35,
    gender='F',
    patient_contact=YES,
    primary_cell=seq('77654312'),
    village_town='molapowabojang',
    kin_details_provided=NO,
    clinician_type='med_officer',
    early_symptoms_date=get_utcnow() - relativedelta(months=1),
    early_symptoms_date_estimated=NO,
    suspected_cancer='head_neck',
    suspicion_level='low',
    performance=0,
    pain_score='0_no_pain',
    last_hiv_result=NEG,
    patient_disposition='return',
    referral_date=get_utcnow() + relativedelta(months=1),
    referral_unit=NOT_APPLICABLE,
    referral_discussed=NOT_APPLICABLE,
    triage_status='routine',
    investigated=NO 
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
    dob=get_utcnow() - relativedelta(years=25),
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
    subject_identifier=None)

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
    age_in_years=25,
    education_level='secondary',
    work_status='no',
    transport_support=NO,
    medical_conditions=NO,
    tests_ordered=NO,
    heard_of_potlako=YES
)

symptomandcareseekingassessment = Recipe(
    SymptomAndCareSeekingAssessment,)

patientcallfollowup = Recipe(
    PatientCallFollowUp,
    encounter_date=get_utcnow().date(),
    start_time=get_utcnow().time(),
    investigations_ordered='blah',
    last_visit_date=get_utcnow() - relativedelta(days=1),
    next_appointment_date=get_utcnow() + relativedelta(months=2)
)

cancerdxtx = Recipe(
    CancerDxAndTx,)

missedvisit = Recipe(
    MissedVisit,)

missedcall = Recipe(
    MissedCall,)

missedcallrecord = Recipe(
    MissedCallRecord,)
