from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, YES, NO, NOT_APPLICABLE, NEG
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import UNSCHEDULED
from model_mommy import mommy

from ..forms import (
    ClinicianCallFollowUpForm, HomeVisitForm, InvestigationsForm, LabTestForm,
    PatientCallInitialForm, PatientStatusForm, PhysicianReviewForm, SMSForm,
    TransportForm, MissedCallForm, MissedVisitForm)
from ..models.list_models import CallAchievements
from ..models import Investigations


class Test_Crf_Creation(TestCase):
    """Test if potlako subject crfs are able to be successfully created."""

    def setUp(self):
        import_holidays()
        subject_screening = mommy.make_recipe(
            'potlako_subject.subjectscreening')
        options = {
            'screening_identifier': subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'version': 1}
        self.consent = mommy.make_recipe(
            'potlako_subject.subjectconsent', **options)
        self.subject_identifier = self.consent.subject_identifier
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code='1000')
        self.subject_visit = mommy.make_recipe(
            'potlako_subject.subjectvisit',
            appointment=self.appointment,
            reason=UNSCHEDULED,)
        self.data = {
            'subject_visit': self.subject_visit,
            'report_datetime': get_utcnow(),
            }

    def test_clinician_call_fu_creation(self):
        form_data = self.data
        form_data.update(
            facility_visited='bokaa_pc',
            call_clinician='Jane',
            facility_unit='OPD',
            visit_type=YES,
            perfomance_status=3,
            pain_score=2,
            patient_disposition='return',
            return_visit_scheduled=YES,
            return_visit_date=get_utcnow() + relativedelta(months=2),
            investigation_ordered=NO,
            triage_status='routine',
            transport_support=NO,
            followup_end_time=(
                datetime.now() + relativedelta(hours=2)).time(),)

        clinician_call_fu = ClinicianCallFollowUpForm(data=form_data)
        self.assertTrue(clinician_call_fu.save())

    def test_home_visit_creation(self):
        form_data = self.data
        form_data.update(
            clinician_name='Jane',
            clinician_type='med_officer',
            facility_clinician_works='bokaa_pc',
            clinician_two_name='John',
            clinician_two_type='med_officer',
            clinician_two_facility='bokaa_pc',
            clinician_three_name='Judy',
            clinician_three_type='med_officer',
            clinician_three_facility='bokaa_pc',
            visit_outcome=ALIVE,
            next_appointment=get_utcnow() + relativedelta(months=2),
            next_ap_facility='bokaa_pc',
            nex_ap_type='return',)

        home_visit = HomeVisitForm(data=form_data)
        self.assertTrue(home_visit.save())

    def test_investigations_creation(self):
        form_data = self.data
        form_data.update(
            facility_ordered='bokaa_pc',
            ordered_date=get_utcnow(),
            lab_tests_ordered=YES,
            pathology_tests_ordered=NO,
            imaging_tests=YES,
            imaging_test_status='ordered',
            imaging_test_type='ultrasound_abdomen',
            bpcc_enrolled=NO,
            end_time=(datetime.now() + relativedelta(hours=2)).time(),)

        investigations = InvestigationsForm(data=form_data)
        self.assertTrue(investigations.save())

        """Test if lab test form is created succesfully"""

        lab_test_data = self.data
        lab_test_data.update(
            investigations=Investigations.objects.all()[0],
            lab_test_type='LFT',
            lab_test_date=get_utcnow() + relativedelta(days=5),
            lab_test_status='specimen_taken',)

        lab_test_form = LabTestForm(data=lab_test_data)
        lab_test_form.full_clean()
        self.assertTrue(lab_test_form.is_valid())

    def test_missed_call_creation(self):
        form_data = self.data
        form_data.update(
            entry_date=get_utcnow(),
            notes='A little bit of notes for future reference.',
            repeat_call=get_utcnow() + relativedelta(months=2),)

        missed_call_form = MissedCallForm(data=form_data)
        self.assertTrue(missed_call_form.save())

    def test_missed_visit_creation(self):
        form_data = self.data
        form_data.update(
            missed_visit_date=get_utcnow(),
            facility_scheduled='bokaa_pc',
            visit_type='referral',
            determine_missed='database',
            inquired=YES,
            inquired_from='patient_called',
            reason_missed='no_transport_fare',
            next_appointment=get_utcnow() + relativedelta(months=2),
            next_ap_facility='bokaa_pc',
            next_ap_type='return',
            home_visit=NO,
            transport_need=YES,
            clinician_name='Ms Jane',)

        missed_visit_form = MissedVisitForm(
            data=form_data)
        self.assertTrue(missed_visit_form.save())

    def test_patient_call_initial(self):
        CallAchievements.objects.create(
            name='communicate_results', short_name='communicate_results')
        CallAchievements.objects.create(
            name='arrange_transportation', short_name='arrange_transportation')
        form_data = self.data
        form_data.update(
            patient_call_time=get_utcnow().time(),
            patient_call_date=get_utcnow(),
            start_time=get_utcnow().time(),
            dob_known=NO,
            patient_contact_residence_change=NO,
            primary_clinic='bokaa_pc',
            patient_contact_change=NO,
            next_of_kin=NO,
            patient_symptoms='aish goa tshosa',
            patient_symptoms_date=get_utcnow() - relativedelta(months=5),
            other_facility=NO,
            facility_number=3,
            facility_previously_visited='kgope_hp',
            previous_facility_period='2months',
            perfomance_status=2,
            pain_score=3,
            hiv_status=NEG,
            cancer_suspicion_known=YES,
            enrollment_clinic_visit_method='I dont know',
            slh_travel='On foot',
            tests_ordered=YES,
            next_appointment_date=get_utcnow() + relativedelta(months=2),
            next_visit_delayed=NO,
            next_appointment_facility='bokaa_pc',
            next_appointment_facility_unit='medicine_ward',
            patient_understanding=YES,
            transport_support=YES,
            call_achievements=CallAchievements.objects.all(),
            clinician_information=NO,
            cancer_probability='high',
            encounter_end_time=(get_utcnow() + relativedelta(hours=1)).time(),
            initial_call_end_time=(
                get_utcnow() + relativedelta(hours=1)).time(),
            call_duration=1,
            )

        patient_call_initial = PatientCallInitialForm(data=form_data)
        self.assertTrue(patient_call_initial.save())

    def test_patient_status_creation(self):
        form_data = self.data
        form_data.update(
            last_encounter=get_utcnow() - relativedelta(months=1),
            sms_due=YES,
            days_from_recent_visit=30,
            physician_flag='Improved',
            bcpp_enrolled=NO,
            deceased=NO,
            calc_hiv_status=NEG,
            missed_calls=1,
            seen_at_marina=YES,
            exit_status='Not exited',
            first_last_visit_days=30,
            missed_visits=0,)

        patient_status = PatientStatusForm(data=form_data)
        self.assertTrue(patient_status.save())

    def test_physician_review_creation(self):
        form_data = self.data
        form_data.update(
            reviewer_name='neo',
            physician_summary='very brief',
            diagnosis_plan='something very helpful, we hope',
            needs_discussion=YES,
            coordinator_summary='another brief sum',
            cancer_eval='complete',
            reason_fu_needed='to help, i assume',
            final_status='confirmed',
            to_be_flagged=YES,)

        physician_review = PhysicianReviewForm(data=form_data)
        self.assertTrue(physician_review.save())

    def test_sms_creation(self):
        form_data = self.data
        form_data.update(
            date_time_form_filled=get_utcnow(),
            next_ap_date=get_utcnow() + relativedelta(months=2),
            date_reminder_sent=get_utcnow() - relativedelta(days=3),
            sms_outcome='patient_sent_sms_received',)

        sms_form = SMSForm(data=form_data)
        self.assertTrue(sms_form.save())

    def test_transport_creation(self):
        form_data = self.data
        form_data.update(
            is_criteria_met=YES,
            qualification='BGCSE',
            housemate='parents',
            car_ownership=NO,
            criteria_met='lives_far',
            next_visit_date=get_utcnow() + relativedelta(months=2),
            visit_facility='bokaa_pc',
            transport_type='cash',
            facility_vehicle_status=NOT_APPLICABLE,
            bus_voucher_status=NOT_APPLICABLE,
            cash_transfer_status='successful_unconfirmed',
            comments='N/A')

        transport_form = TransportForm(data=form_data)
        transport_form.full_clean()
        self.assertTrue(transport_form.save())
