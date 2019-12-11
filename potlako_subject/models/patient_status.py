from django.db import models


class PatientStatus(models.Model):

    last_encounter = models.CharField(
        max_length=25,)

    sms_due = models.CharField(
        verbose_name='Due for SMS prior to visit',
        max_length=15,)

    days_from_recent_visit = models.PositiveIntegerField(
        verbose_name='Days from most recent visit',)

    physician_flag = models.CharField(
        max_length=10,)

    bpcc_bid_entered = models.CharField(
        max_length=10,)

    bcpp_enrolled = models.CharField(
        verbose_name='Marked BCPP enrolled',
        max_length=10,)

    deceased = models.CharField(
        max_length=10,)

    days_from_death_report = models.PositiveIntegerField()

    calc_hiv_status = models.CharField(
        verbose_name='Calculated HIV status',
        max_length=15,)

    missed_calls = models.IntegerField(
        verbose_name='Number of missed calls',)

    seen_at_marina = models.CharField(
        max_length=10,)

    exit_status = models.CharField(
        max_length=10)

    first_last_visit_days = models.PositiveIntegerField(
        verbose_name='Days from first to last visit in Potlako (if not '
                     'exited, days to today)',)

    missed_visits = models.PositiveIntegerField(
        verbose_name='Number of missed visits',)

    class Meta:
        app_label = 'potlako_subject'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
