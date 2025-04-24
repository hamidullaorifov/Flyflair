from django.db import models

def generate_handover_id(shift_type, shift_date):
    return f"{shift_type}-{shift_date}"


class Handover(models.Model):
    handover_id = models.CharField(max_length=13, primary_key=True)
    shift_date = models.DateField()
    shift = models.CharField(max_length=2)
    dispatcher_name = models.CharField(max_length=100)
    chief_duty_name = models.CharField(max_length=100)
    shift_highlights = models.TextField()
    non_standard_flights = models.JSONField(default=list)
    naifr = models.JSONField(default=list)
    aog = models.JSONField(default=list)
    comat_flights = models.JSONField(default=list)
    fob_created_aog = models.BooleanField(default=False)
    remarks_created_com = models.BooleanField(default=False)
    fuel_payload_critical = models.TextField(null=True, blank=True)
    weather_issues = models.TextField(null=True, blank=True)
    operational_notams = models.TextField(null=True, blank=True)
    enroute_weather = models.TextField(null=True, blank=True)
    mels = models.TextField(null=True, blank=True)
    cdd_network_summary = models.TextField(null=True, blank=True)
    misc = models.TextField(null=True, blank=True)
    it_issues = models.TextField(null=True, blank=True)
    navblue_tickets = models.TextField(null=True, blank=True)
    procedural_changes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Automatically create ID only if not provided"""
        if not self.handover_id:  # Only generate if it's not already set
            self.handover_id = generate_handover_id(self.shift, self.shift_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.shift}-{self.shift_date}-{self.dispatcher_name}"


# class NonStandardFlight(models.Model):
#     handover = models.ForeignKey(Handover, on_delete=models.CASCADE, related_name='non_standard_flights')
#     flight = models.CharField(max_length=20, blank=True, null=True)
#     alternate = models.CharField(max_length=20, blank=True, null=True)
#     remarks = models.TextField(blank=True, null=True)
