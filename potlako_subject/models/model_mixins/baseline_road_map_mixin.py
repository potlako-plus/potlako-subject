from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from ...constants import UNSURE
from ..clinician_call_enrollment import ClinicianCallEnrollment

class BaselineRoadMapMixin:
    """A class to gather all values from Clinician Call Enrollment, 
    Patient Call Initial, Investigations Ordered, Investigations Resulted
    to build the Baseline Roadmap.
    """

    def __init__(self, subject_identifier=None):
        self.subject_identifier = subject_identifier
        self.baseline_dict = {'display_summary': True,
                              'cliniciancallenrollment': self.clinician_call_attrs}
        
        non_crfs = ['potlako_subject.baselineclinicalsummary',
                    'potlako_subject.navigationsummaryandplan']
        
        attrs_list = [['symptoms_summary', 'cancer_concern', 'cancer_probability'],
                      ['diagnostic_plan',]]
        
        
                 
        crfs_list = ['potlako_subject.cancerdiagnosisandtreatmentassessment',
                     'potlako_subject.symptomandcareseekingassessment',
                     'potlako_subject.patientcallinitial',
                     'potlako_subject.investigationsordered',
                     'potlako_subject.investigationsresulted',
                      'potlako_subject.medicalconditions']
     
    
    
        crf_attrs_list =[['symptoms_summary', 'cancer_evaluation', 'diagnoses_date',
                          'diagnoses_date_estimated', 'diagnosis_date_estimation',
                          'cancer_treatment', 'treatment_description'],
                         ['first_visit_prompt', 'cause_assumption', 'symptoms_concern'],
                         ['report_datetime', 'age_in_years', 'hiv_status',
                          'patient_symptoms', 'perfomance_status', 'pain_score'],
                         ['tests_ordered_type', ],
                         ['diagnosis_results', 'cancer_type', 'cancer_stage']]
                
    
        for crf_model, attrs in zip(crfs_list, crf_attrs_list):
            crf_objs = django_apps.get_model(crf_model).objects.filter(
                subject_visit__subject_identifier=self.subject_identifier)
            
            if crf_objs:
                crf_obj = crf_objs.order_by('created')[0]
                crf_dict={}
                
                for attr in attrs:
                    value = getattr(crf_obj, attr)
                    crf_dict.update({attr:value})
                    
                if crf_dict:
                    self.baseline_dict.update({crf_model.split('.')[1]: crf_dict})
        
        for crf_model, attrs in zip(non_crfs, attrs_list):
            crf_cls = django_apps.get_model(crf_model)
            try:
                crf_obj = crf_cls.objects.get(subject_identifier=self.subject_identifier)
            except crf_cls.DoesNotExist:
                pass
            else:
                crf_dict={}
                
                for attr in attrs:
                    value = getattr(crf_obj, attr)
                    crf_dict.update({attr:value})
                    
                if crf_dict:
                    self.baseline_dict.update({crf_model.split('.')[1]: crf_dict})
        
                    
    @property
    def screening_identifier(self):
        screening_cls = django_apps.get_model('potlako_subject.subjectscreening')
        try:
            screening_obj = screening_cls.objects.get(subject_identifier=self.subject_identifier)
        except screening_cls.DoesNotExist:
            return None
        else:
            return screening_obj.screening_identifier
        
    
    @property
    def clinician_call_attrs(self):
        """Extract values required for Baseline Map from Clinician Call
        Enrollment model.
        """
        enrollment_dict = {}
        attributes = ['age_in_years', 'suspected_cancer', 'suspected_cancer_other',
                      'gender', 'suspicion_level', 'last_hiv_result']

        try:
            clinician_call_obj = ClinicianCallEnrollment.objects.get(
            screening_identifier=self.screening_identifier)
        except ObjectDoesNotExist as e:
            raise(e)
        else:
            for attr in attributes:
                value = getattr(
                        clinician_call_obj, attr)

                if attr == 'suspected_cancer' and value == UNSURE:
                    value = getattr(
                        clinician_call_obj, 'suspected_cancer_unsure')

                enrollment_dict.update({attr:value})
        return enrollment_dict



