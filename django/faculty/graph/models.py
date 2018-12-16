from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    timing = models.DateTimeField(default=timezone.now)
    data = models.DecimalField(max_digits=4, decimal_places=0)

    def __str__(self):
        return str(self.timing) + " - " + str(self.data)

    class Meta:
        ordering = ['-timing']