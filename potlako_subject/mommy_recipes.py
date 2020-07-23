from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, YES, NO, ON_STUDY, PARTICIPANT
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import ClinicianCallEnrollment, PatientCallInitial
from .models import SubjectConsent, SubjectScreening, SubjectVisit

fake = Faker()

cliniciancallenrollment = Recipe(
    ClinicianCallEnrollment,
    cancer_suspect=YES,
    first_name=fake.first_name,
    last_name=fake.last_name,
    gender='F',
    age_in_years=25,
    national_identity=seq('123425678', increment_by=1),
    primary_cell='77654312',
    secondary_cell='77654312'
)

subjectscreening = Recipe(
    SubjectScreening,
    has_diagnosis=YES,
    enrollment_site='princess_marina_hospital'
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
    identity=seq('123425678'),
    confirm_identity=seq('123425678'),
    identity_type='OMANG',
    is_dob_estimated='-',
    version='1'
)

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
    tests_ordered='blah'
)
