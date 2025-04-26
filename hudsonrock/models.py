from django.db import models

class Credential(models.Model):
    url = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

class HudsonRockData(models.Model):
    stealer = models.CharField(max_length=255)
    stealerFamily = models.CharField(max_length=255)
    dateUploaded = models.DateTimeField()
    employeeAt = models.JSONField()  # Stores array of strings
    clientAt = models.JSONField()    # Stores array of strings
    dateCompromised = models.DateTimeField()
    ip = models.CharField(max_length=50)
    computerName = models.CharField(max_length=255)
    operatingSystem = models.CharField(max_length=255)
    malwarePath = models.CharField(max_length=255)
    antiviruses = models.JSONField()  # Stores array of strings
    credentials = models.JSONField()  # Stores array of credential objects
    data_type = models.CharField(max_length=50)  # Custom field for filtering

    class Meta:
        db_table = 'hudson_rock_data'
