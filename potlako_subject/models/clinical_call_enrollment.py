from django.db import models


class ClinicalCallEnrollment(models.Model):
    
    record_id = models.CharField(
        verbose_name="Record Id",
        max_length=50,
        unique=True)
    
    start_time = models.DateTimeField(
        verbose_name="Clinical Enrollment Call: Start Time")
    
    date = models.DateField(
        verbose_name="Date of communication of patient to coordinator")
    
    clinician = models.CharField(
        verbose_name=   "Name of clinician spoken to on the phone "
                        "for initial call")
    
    