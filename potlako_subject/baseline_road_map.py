from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .models import ClinicianCallEnrollment


class BaselineRoadMap:
    """A class to gather all values from Clinician Call Enrollment, 
    Patient Call Initial, Investigations Ordered, Investigations Resulted
    to build the Baseline Roadmap.
    """

    def __init__(self, subject_identifier=None, subject_visit=None):

        baseline_dict = self.get_clinician_call_attrs(
            subject_identifier=subject_identifier)

        crfs_list = ['potlako_subject.patientcallinitial',
                     'potlako_subject.investigationsordered',
                     'potlako_subject.investigationsresulted',
                      'potlako_subject.medicalconditions']

        attrs_list = [['report_datetime', 'age_in_years', 'hiv_status',
                      'patient_symptoms', 'perfomance_status', 'pain_score'],
                       ['tests_ordered_type', ],
                       ['diagnosis_results', 'cancer_type', 'cancer_stage']]

        for crf_cls, attrs in zip(crfs_list, attrs_list):
            crf_cls = django_apps.get_model(crf_cls)
            crf_dict = self.get_crf_attrs(subject_visit=subject_visit,
                               crf_cls, attrs)
            baseline_dict.update(crf_dict)

    def get_clinician_call_attrs(self, subject_identifier=None):
        """Extract values required for Baseline Map from Clinician Call
        Enrollment model.
        """

        enrollment_dict = {}
        attributes = ['suspected_cancer', 'suspected_cancer_other',
                      'gender', 'suspicion_level']

        try:
            clinician_call_obj = ClinicianCallEnrollment.objects.get(
            subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            for attr in attributes:
                value = getattr(clinician_call_obj)
                enrollment_dict.update({attr:value})

        return enrollment_dict

    def get_crf_attrs(self, subject_visit=None, model_cls, *attributes):
        """Extract values required for Baseline Map from model.
        """

        crf_dict = {}

        try:
            model_obj = model_cls.objects.get(
                subject_visit=subject_visit)
        except model_cls.DoesNotExist:
            return None
        else:
            for attr in attributes:
                value = getattr(model_obj)
                crf_dict.update({attr:value})

        return crf_dict

