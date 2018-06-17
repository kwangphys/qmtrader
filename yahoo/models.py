from django.db import models as dm
from getpass import getuser


class DatedModel(dm.Model):

    updated_on = dm.DateTimeField(auto_now_add=True)
    updated_by = dm.CharField(max_length=64, default=getuser())

    class Meta:
        abstract = True


class EarningsCalendar(DatedModel):

    ticker = dm.CharField(max_length=16, null=False, blank=False)
    full_name = dm.CharField(max_length=255)
    fiscal_quarter_ending = dm.CharField(max_length=16, null=False, blank=False)
    earnings_date = dm.DateField(null=False)
    time = dm.CharField(max_length=32)
    consensus_eps_forecast = dm.FloatField(null=True)
    n_estimates = dm.IntegerField()
    is_confirmed = dm.BooleanField()
    source = dm.CharField(max_length=16)

