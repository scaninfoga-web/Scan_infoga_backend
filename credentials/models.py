from django.db import models

class Credential(models.Model):
    email = models.EmailField(unique=True, max_length=320)
    password = models.CharField(max_length=1024)

    def __str__(self):
        return self.email
