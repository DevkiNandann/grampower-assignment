from django.db import models
from django.utils import timezone


class Meter(models.Model):
    meter_address = models.CharField(max_length=16)
    created_at = models.DateTimeField(default=timezone.now)


class Reading(models.Model):
    meter = models.ForeignKey(
        "Meter",
        on_delete=models.CASCADE,
        related_name="reading_meter",
    )
    voltage = models.FloatField()
    active_power = models.FloatField()
    apparent_power = models.FloatField()
    active_energy = models.FloatField()
    apparent_energy = models.FloatField()
    phase_current = models.FloatField()
    neutral_current = models.FloatField()
    frequency = models.FloatField()
    power_factor = models.FloatField()
    meter_time = models.DateTimeField()
