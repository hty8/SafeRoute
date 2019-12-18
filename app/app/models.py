from django.contrib.gis.db import models


class Scores(models.Model):
    gid = models.AutoField(primary_key=True)
    location = models.CharField(max_length=254, blank=True, null=True)
    latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'scores'