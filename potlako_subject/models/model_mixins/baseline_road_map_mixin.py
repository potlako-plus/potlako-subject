from django.apps import apps as django_apps
from django.db.models import Q

from ..clinician_call_enrollment import ClinicianCallEnrollment
from ..patient_call_followup import PatientCallFollowUp


class BaselineRoadMapMixin:
    """A class to gather all values from Clinician Call Enrollment,
    Patient Call Initial, Investigations Ordered, Investigations Resulted
    to build the Baseline Roadmap.
    """

    def __init__(self, subject_identifier=None):
        self.subject_identifier = subject_identifier
        self.baseline_dict = {}
        self.baseline_dict.update(self.clinician_call)
        self.baseline_dict.update(self.crfs_dict)
        self.baseline_dict.update(self.non_crfs_dict)
        if self.extra_symptoms_description:
            self.baseline_dict.update(self.extra_symptoms_description)

    @property
    def screening_identifier(self):
        
        screening_identifier = None
        
        subject_consent_cls = django_apps.get_model('potlako_subject.subjectconsent')
        screening_cls = django_apps.get_model('potlako_subject.subjectscreening')

        try:
            screening_obj = screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
            
        except screening_cls.DoesNotExist:
            pass
        
        except screening_cls.MultipleObjectsReturned:
            """
            If two screenings are returned get the screening identifier from
            the consent
            """
            try:
                subject_consent_obj = subject_consent_cls.objects.get(
                    subject_identifier=self.subject_identifier)
                
            except subject_consent_cls.MultipleObjectsReturned:
                pass
            
            else:
                screening_identifier = subject_consent_obj.screening_identifier
        else:
            screening_identifier = screening_obj.screening_identifier
        
        return screening_identifier

    @property
    def clinician_call(self):
        """Extract values required for Baseline Map from Clinician Call
        Enrollment model.
        """

        try:
            clinician_call_obj = ClinicianCallEnrollment.objects.get(
                screening_identifier=self.screening_identifier)
        except ClinicianCallEnrollment.DoesNotExist:
            return {}
        else:
            return {'cliniciancallenrollment': clinician_call_obj}

    @property
    def extra_symptoms_description(self):
        """Extract all  new_symptoms_description required for Baseline Map from all Patient Call
           Followup models.
        """

        patient_call_fu_objs = PatientCallFollowUp.objects.filter(
            ~Q(new_complaints_description=''),
            subject_visit__subject_identifier=self.subject_identifier)
        if patient_call_fu_objs:
            complaints = patient_call_fu_objs.latest('report_datetime')

            return {'extra_symptoms_description': complaints.new_complaints_description}

    @property
    def crfs_dict(self):
        crfs_list = ['potlako_subject.cancerdxandtx',
                     'potlako_subject.symptomandcareseekingassessment',
                     'potlako_subject.patientcallinitial',
                     'potlako_subject.investigationsordered',
                     'potlako_subject.investigationsresulted',
                     'potlako_subject.medicaldiagnosis']

        crf_dict = {}
        for crf_model in crfs_list:
            crf_objs = django_apps.get_model(crf_model).objects.filter(
                subject_visit__subject_identifier=self.subject_identifier)

            if crf_objs:
                crf_obj = crf_objs.order_by('created')[0]
                crf_dict.update({crf_model.split('.')[1]: crf_obj})
        return crf_dict

    @property
    def non_crfs_dict(self):

        non_crfs = ['potlako_subject.baselineclinicalsummary',
                    'potlako_subject.navigationsummaryandplan']

        crf_dict = {}

        for crf_model in non_crfs:
            crf_cls = django_apps.get_model(crf_model)
            try:
                crf_obj = crf_cls.objects.get(subject_identifier=self.subject_identifier)
            except crf_cls.DoesNotExist:
                pass
            else:
                crf_dict.update({crf_model.split('.')[1]:
                                crf_obj})
        return crf_dict
