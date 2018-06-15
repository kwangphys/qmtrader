from django.db import models
from getpass import getuser


class DatedModel(models.Model):

    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=64, default=getuser())

    class Meta:
        abstract = True


class NasdaqEarningsCalendar(DatedModel):

    ticker = models.CharField(max_length=16, null=False, blank=False)
    full_name = models.CharField(max_length=255)
    fiscal_quarter_ending = models.CharField(max_length=16, null=False, blank=False)
    earnings_date = models.DateField(null=False)
    time = models.CharField(max_length=32)
    consensus_eps_forecast = models.FloatField()
    n_estimates = models.IntegerField()
    is_confirmed = models.BooleanField()

