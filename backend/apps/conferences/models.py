from django.db import models

class Conference(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    isactive = models.BooleanField(default=True)
    note = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "CONFERENCE"