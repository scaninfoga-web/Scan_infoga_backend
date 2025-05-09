from django.db import models
from django.conf import settings

# Create your models here.

class TokenUpdationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.updated_at}"

    class Meta:
        app_label = 'ghunt_util_app'
