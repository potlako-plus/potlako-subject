from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, INCOMPLETE, NO
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy
from edc_appointment.models import Appointment
from potlako_subject.models.onschedule import OnSchedule


class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.clinician_call = mommy.make_recipe(
            'potlako_subject.cliniciancallenrollment',
            screening_identifier='12345')

        self.subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening',
            screening_identifier=self.clinician_call.screening_identifier)

        self.subject_consent = mommy.make_recipe(
            'potlako_subject.subjectconsent',
            screening_identifier=self.clinician_call.screening_identifier,
            consent_datetime=get_utcnow() - relativedelta(days=3))
        
        self.onschedule_obj = OnSchedule.objects.get(
            subject_identifier=self.subject_consent.subject_identifier)

        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')

        self.subject_visit_1000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=2),
            appointment=self.appointment_1000)
        
        self.patient_call_initial = mommy.make_recipe(
            'potlako_subject.patientcallinitial',
            subject_visit=self.subject_visit_1000,
            transport_support=YES,
            next_appointment_date=get_utcnow())
        
        self.appointment_1000_1 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000',
            visit_code_sequence='1')
 
        self.subject_visit_1000_1 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=2),
            appointment=self.appointment_1000_1)
    
    
    def test_transport_form_required_intervention_subject(self):
        self.patient_call_initial.transport_support=YES
        self.patient_call_initial.save()
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)
        
    def test_transport_form_not_required_control_subject(self):
        self.onschedule_obj.community_arm = 'Standard of Care'
        self.onschedule_obj.save()
        self.clinician_call.facility = 'otse_clinic'
        self.clinician_call.save()
        
        self.patient_call_initial.transport_support=YES
        self.patient_call_initial.save()
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)
        
    def test_transport_form_not_required_control_subject2(self):
        self.onschedule_obj.community_arm = 'Standard of Care'
        self.onschedule_obj.save()
        self.clinician_call.facility = 'otse_clinic'
        self.clinician_call.save()
        
        self.patient_call_initial.transport_support=NO
        self.patient_call_initial.save()

        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)
    


    def test_transport_form_not_required_intervention_subject(self):
        self.patient_call_initial.transport_support=NO
        self.patient_call_initial.save()
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.transport',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_medical_diagnosis_form_not_required_subject(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.medicaldiagnosis',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_medical_diagnosis_form_required_subject(self):
        self.patient_call_initial.medical_conditions=YES
        self.patient_call_initial.save()
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.medicaldiagnosis',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_tests_ordered_form_not_required_subject(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_tests_ordered_form_required_subject(self):
        self.patient_call_initial.tests_ordered='ordered'
        self.patient_call_initial.save()
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)
    
    def test_tests_ordered_and_resulted_form_required_subject(self):
        self.patient_call_initial.tests_ordered='ordered_and_resulted'
        self.patient_call_initial.save()
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsresulted',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_investigations_ordered_form_not_required_subject(self):
        self.appointment_1000.appt_status = INCOMPLETE
        self.appointment_1000.save()
        
        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.subject_visit_1000_1)
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='1').entry_status, NOT_REQUIRED)
 
    def test_investigations_ordered_form_required_subject(self):
        self.appointment_1000.appt_status = INCOMPLETE
        self.appointment_1000.save()
        
        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.subject_visit_1000_1,
            investigations_ordered='ordered')
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='1').entry_status, REQUIRED)
    
    def test_investigations_ordered_and_resulted_form_required_subject(self):
        self.appointment_1000.appt_status = INCOMPLETE
        self.appointment_1000.save()
        
        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.subject_visit_1000_1,
            investigations_ordered='ordered_and_resulted')
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsordered',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='1').entry_status, REQUIRED)
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsresulted',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='1').entry_status, REQUIRED)
 
    def test_investigations_resulted_form_not_required_subject(self):
        self.appointment_1000.appt_status = INCOMPLETE
        self.appointment_1000.save()
        
        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.subject_visit_1000_1)
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsresulted',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='1').entry_status, NOT_REQUIRED)
 
    def test_investigations_resulted_form_required_subject(self):
        self.appointment_1000.appt_status = INCOMPLETE
        self.appointment_1000.save()
        
        mommy.make_recipe(
            'potlako_subject.patientcallfollowup',
            subject_visit=self.subject_visit_1000_1,
            investigations_ordered='ordered_and_resulted')
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.investigationsresulted',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='1').entry_status, REQUIRED)
        
    def test_missed_visit_metadata(self):
        self.appointment_2000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='2000')

        self.subject_visit_2000 = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=2),
            reason = 'missed_quarterly_visit',
            appointment=self.appointment_2000)
        
        self.assertEqual(
            CrfMetadata.objects.get(
                model='potlako_subject.missedvisit',
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

#     @tag('hv')
#     def test_missed_home_visit_metadata(self):
#         self.appointment_2000 = Appointment.objects.get(
#             subject_identifier=self.subject_consent.subject_identifier,
#             visit_code='2000')
# 
#         self.subject_visit_2000 = mommy.make_recipe(
#             'potlako_subject.subjectvisit',
#             subject_identifier=self.subject_consent.subject_identifier,
#             report_datetime=get_utcnow() - relativedelta(days=2),
#             appointment=self.appointment_2000)
#         
#         self.missed_call = mommy.make_recipe(
#             'potlako_subject.missedcall',
#             report_datetime=get_utcnow() - relativedelta(days=2),
#             subject_visit=self.subject_visit_2000)
#         
#         mommy.make_recipe(
#             'potlako_subject.missedcallrecord',
#             missed_call=self.missed_call)
#         
#         mommy.make_recipe(
#             'potlako_subject.missedcallrecord',
#             missed_call=self.missed_call)
#         
#         mommy.make_recipe(
#             'potlako_subject.missedcallrecord',
#             missed_call=self.missed_call)
#         
#         self.assertEqual(
#             CrfMetadata.objects.get(
#                 model='potlako_subject.homevisit',
#                 subject_identifier=self.subject_consent.subject_identifier,
#                 visit_code='2000').entry_status, REQUIRED)
