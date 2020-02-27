from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, YES, NO, ON_STUDY, PARTICIPANT
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import SubjectConsent, SubjectScreening, SubjectVisit


fake = Faker()

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
    first_name='JANE',
    last_name='DOE',
    initials='JD',
    gender='F',
    identity=seq('123425678'),
    confirm_identity=seq('123425678'),
    identity_type='OMANG',
    is_dob_estimated='-',
    is_incarcerated=NO,
)

subjectvisit = Recipe(
    SubjectVisit,
    report_datetime=get_utcnow(),
    reason=SCHEDULED,
    study_status=ON_STUDY,
    survival_status=ALIVE,
    info_source=PARTICIPANT)
