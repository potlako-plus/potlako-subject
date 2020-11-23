from dateutil.relativedelta import relativedelta
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy


class SubjectHelperMixin:

    def create_enrollment(self, facility):
        import_holidays()

        clinicial_call_enrolment = self.subject_screening = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment',
            facility=facility)

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier=clinicial_call_enrolment.screening_identifier)

        self.options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow() - relativedelta(days=5),
            'first_name': clinicial_call_enrolment.first_name,
            'last_name': clinicial_call_enrolment.last_name,
            'identity': clinicial_call_enrolment.national_identity,
            'confirm_identity': clinicial_call_enrolment.national_identity,
            'version': '1'}

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            **self.options)

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectlocator',
            subject_identifier=self.subject_consent.subject_identifier)

        return self.subject_consent.subject_identifier

    def create_visit_1000(self, subject_identifier):

        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='1000')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=subject_visit)

        mommy.make_recipe(
            'potlako_subject.symptomandcareseekingassessment',
            subject_visit=subject_visit)

    def create_visit_2000(self, subject_identifier):

        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='2000')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=subject_visit)

    def create_followup_visit(self, subject_identifier):
        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='2000',
            visit_code_sequence='1')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=6),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=subject_visit)

        mommy.make_recipe(
            'potlako_subject.cancerdxandtx',
            subject_visit=subject_visit)

    def create_visit_3000(self, subject_identifier):

        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='3000')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=subject_visit)
