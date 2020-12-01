from dateutil.relativedelta import relativedelta
from edc_appointment.models import Appointment
from edc_appointment.constants import COMPLETE_APPT
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy


class SubjectHelperMixin:

    def create_enrollment(self, facility, **kwargs):
        import_holidays()

        clinicial_call_enrolment = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment',
            facility=facility,
            **kwargs)
        
        mommy.make_recipe(
            'potlako_subject.nextofkin',
            clinician_call_enrollemt=clinicial_call_enrolment,)

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
        
        mommy.make_recipe(
            'potlako_subject.verbalconsent',)

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
            report_datetime=get_utcnow(),
            appointment=appt)
        
        mommy.make_recipe(
            'potlako_subject.baselineclinicalsummary',
            subject_identifier=subject_identifier,)
        
        mommy.make_recipe(
            'potlako_subject.baselineroadmap',
            subject_identifier=subject_identifier,)
        
        nav_plan = mommy.make_recipe(
            'potlako_subject.navigationsummaryandplan',
            subject_identifier=subject_identifier,)
        
        mommy.make_recipe(
            'potlako_subject.evaluationtimeline',
            navigation_plan=nav_plan,)

        patient_initial = mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.previousfacilityvisit',
            patient_call_initial=patient_initial)
        
        symptom_care = mommy.make_recipe(
            'potlako_subject.symptomandcareseekingassessment',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.symptomassessment',
            symptom_care_seeking=symptom_care)
        
        medical_diagnosis = mommy.make_recipe(
            'potlako_subject.medicaldiagnosis',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.medicalconditions',
            medical_diagnosis=medical_diagnosis)
        
        appt.appt_status = COMPLETE_APPT
        appt.save()


    def create_visit_2000(self, subject_identifier):

        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='2000')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appt)

        patient_call_fu = mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.facilityvisit',
            patient_call_followup=patient_call_fu)
        
        mommy.make_recipe(
            'potlako_subject.cancerdxandtx',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.homevisit',
            subject_visit=subject_visit)
        
        investigations_oredered = mommy.make_recipe(
            'potlako_subject.investigationsordered',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.labtest',
            investigations=investigations_oredered)
        
        mommy.make_recipe(
            'potlako_subject.investigationsresulted',
            subject_visit=subject_visit)
        
        appt.appt_status = COMPLETE_APPT
        appt.save()

    def create_followup_visit(self, subject_identifier):
        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='2000',
            visit_code_sequence='1')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=subject_visit,
            transport_support=YES)
        
        missed_call = mommy.make_recipe(
            'potlako_subject.missedcall',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.transport',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.missedcallrecord',
            missed_call=missed_call)
        
        appt.appt_status = COMPLETE_APPT
        appt.save()
        
    def create_followup_missed_visit(self, subject_identifier):
        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='2000',
            visit_code_sequence='2')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.missedvisit',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.sms',
            subject_identifier=subject_identifier)
        
        appt.appt_status = COMPLETE_APPT
        appt.save()
        

    def create_visit_3000(self, subject_identifier):

        appt = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code='3000')

        subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appt)

        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.cancerdxandtx',
            subject_visit=subject_visit)
        
        mommy.make_recipe(
            'potlako_subject.cancerdxandtxendpoint',
             subject_identifier=subject_identifier,)
        
        mommy.make_recipe(
            'potlako_subject.symptomsandcareseekingendpoint',
             subject_identifier=subject_identifier,)
        appt.appt_status = COMPLETE_APPT
        appt.save()